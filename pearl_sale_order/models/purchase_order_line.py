from odoo import models, fields, api
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    brand_id = fields.Many2one('product.brand', related='product_id.brand_id')
    product_categ_id= fields.Many2one('product.category', related='product_id.categ_id')
    product_tag_ids = fields.Many2many('product.tag', related='product_id.product_tag_ids')
    image = fields.Image(compute='_compute_ava_quantity')
    quantity_available = fields.Float(compute='_compute_ava_quantity')

    @api.depends('product_id')
    def _compute_ava_quantity(self):
        for rec in self:
            if rec.product_id:
                product = rec.sudo().env['product.product'].browse(rec.product_id.id)
                ava_qty = product.sudo().qty_available
                image = product.sudo().image_1920
                rec.quantity_available = ava_qty
                rec.image = image
            else:
                rec.quantity_available = 0.0
                rec.image = False

