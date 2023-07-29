from odoo import models, fields, api, _


class SaleChannel(models.Model):
    _name = "sale.channel"
    _description = "The Sale Channels"
    _rec_name = "name"
    _sql_constraints = [
        (
            "code_unique",
            "unique(code)",
            _("Code value must be unique!"),
        )
    ]

    name = fields.Char()
    code = fields.Char()
