from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    sale_channel_id = fields.Many2one("sale.channel")


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.constrains("product_id", "product_uom_qty")
    def check_product_chanel_client_quota(self):
        for rec in self:
            date_order = rec.order_id.date_order.date()
            context = [
                ("product_id", "=", rec.product_id.name),
                ("partner_id", "=", rec.order_id.partner_id.id),
                ("start_date", "<=", date_order),
                ("end_date", ">=", date_order),
            ]
            sale_quotas = self.env["sale.quota"].search(context)
            if len(sale_quotas) == 1:
                if sale_quotas.available_amount > rec.product_uom_qty:
                    sale_quotas.update(
                        {"sold_amount": sale_quotas.sold_amount + rec.product_uom_qty}
                    )
                else:
                    raise UserError(
                        _(
                            f"No se puede confirmar la venta porque sobrepasa el cupo de venta para el producto: {rec.product_id.name}"
                        )
                    )
            elif len(sale_quotas) > 1:
                sale_quota = self.env["sale.quota"].search(
                    context, order="create_date", limit=1
                )
                if rec.product_uom_qty < sale_quota.available_amount:
                    sale_quota.update(
                        {"sold_amount": sale_quota.sold_amount + rec.product_uom_qty}
                    )
                else:
                    total_available = sum(sq.available_amount for sq in sale_quotas)
                    if total_available > rec.product_uom_qty:
                        requested_qty = rec.product_uom_qty
                        for sq in sale_quotas:
                            if requested_qty >= sq.available_amount:
                                requested_qty -= sq.available_amount
                                sq.update({"sold_amount": sq.available_amount})
                            else:
                                sq.update({"sold_amount": requested_qty})
                                requested_qty = 0
                            if requested_qty == 0:
                                break
                    else:
                        raise UserError(
                            _(
                                f"No se puede confirmar la venta porque sobrepasa los cupos de venta para el producto {rec.product_id.name} "
                            )
                        )
