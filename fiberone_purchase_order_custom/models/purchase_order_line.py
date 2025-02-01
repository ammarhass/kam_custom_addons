from odoo import models, fields, api


class PurchaseOrderLine(models.Model):

    _inherit = 'purchase.order.line'

    eg_code = fields.Char(related='product_id.eg_code')
    number_part = fields.Char(related='product_id.number_part')
    manufactured_company = fields.Char(related='product_id.manufactured_company')