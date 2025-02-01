from odoo import models, fields, api


class ImportSaleOrder(models.Model):
    _inherit = 'sale.order'

    partner_id = fields.Many2one(
        domain="[('type', '!=', 'private'), ('company_id', '=', company_id), ('is_customer', '=', True), ('active', '=', True)]",)
