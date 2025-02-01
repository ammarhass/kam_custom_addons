from odoo import models, fields, api


class ImportPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    partner_id = fields.Many2one(
        domain="[('company_id', '=', company_id), ('is_vendor', '=', True), ('active', '=', True)]",
    )
