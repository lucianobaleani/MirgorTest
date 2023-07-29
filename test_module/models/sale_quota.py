from odoo import models, fields, api


class SaleQuota(models.Model):
    _name = "sale.quota"
    _description = "Sale Quotas"
    _rec_name = "sale_channel_id"

    @api.depends("sale_quota", "sold_amount")
    def _compute_available_amount(self):
        for rec in self:
            amount = rec.sale_quota - rec.sold_amount
            rec.update({"available_amount": amount})

    sale_channel_id = fields.Many2one("sale.channel")
    product_id = fields.Many2one("product.product")
    partner_id = fields.Many2one("res.partner")
    start_date = fields.Date()
    end_date = fields.Date()
    sale_quota = fields.Integer(default=0)
    sold_amount = fields.Integer(default=0)
    available_amount = fields.Integer(compute="_compute_available_amount")
