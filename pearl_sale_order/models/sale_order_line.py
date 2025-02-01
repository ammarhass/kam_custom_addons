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


    def prepare_invoice_line(self, invoice):
        invoice_line_vals = super(SaleOrderLine, self).prepare_invoice_line(invoice)

        # Add custom fields to invoice_line_vals
        invoice_line_vals.update({
            'brand_id': self.brand_id.id,
        })

        return invoice_line_vals