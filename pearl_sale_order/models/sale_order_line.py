from pydoc import browse

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    brand_id = fields.Many2one('product.brand', related='product_id.brand_id')
    packaging_qty = fields.Float(related='product_packaging_id.qty')
    product_categ_id = fields.Many2one('product.category', related='product_id.categ_id')
    product_tag_ids = fields.Many2many('product.tag', related='product_id.product_tag_ids')
    can_edit_price = fields.Boolean(
        compute='_compute_can_edit_price',
        store=False
    )
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

    @api.depends('product_id')
    def _compute_can_edit_price(self):
        """Compute if the user belongs to the allowed group."""
        allowed_group = self.env.ref('pearl_sale_order.sale_order_price_unit_group')
        for record in self:
            record.can_edit_price = allowed_group in self.env.user.groups_id


    # @api.constrains('product_uom_qty')
    # def _constrain_product_quantity(self):
    #     for rec in self:
    #         if rec.product_uom_qty > rec.product_id.qty_available:
    #             raise ValidationError(_('The available Quantity of product ({}) is {}'.format(rec.product_id.name, rec.product_id.qty_available)))

    @api.onchange('product_id', 'product_uom_qty')
    def _onchange_product_quantity(self):
        for rec in self:
            if rec.product_id:
                if rec.product_uom_qty > rec.product_id.qty_available:
                    raise ValidationError(_('The available Quantity of product ({}) is {}'.format(rec.product_id.name, rec.product_id.qty_available)))

    @api.constrains('price_total')
    def _constrain_price_total(self):
        self = self.sudo()
        for rec in self:
            if rec.price_total:
                if rec.product_id:
                    if rec.price_total < rec.product_id.standard_price * rec.product_uom_qty:
                        raise ValidationError(
                            _('The Unit price of the product[{}] (include discount) must be greater than the cost price'.format(rec.product_id.name)))



