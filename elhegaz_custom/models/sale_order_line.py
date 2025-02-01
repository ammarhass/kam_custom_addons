from odoo import models, fields, api


class InheritSaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    units_count = fields.Integer()