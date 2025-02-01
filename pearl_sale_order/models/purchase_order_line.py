from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    brand_id = fields.Many2one('product.brand', related='product_id.brand_id')
    product_categ_id= fields.Many2one('product.category', related='product_id.categ_id')
    product_tag_ids = fields.Many2many('product.tag', related='product_id.product_tag_ids')