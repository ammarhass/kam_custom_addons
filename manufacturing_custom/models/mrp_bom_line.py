from odoo import models, fields, api


class InheritMrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    unbuild_order_id = fields.Many2one('mrp.unbuild')
    product_qty_percentage = fields.Float(compute='_compute_product_qty_percentage', inverse='_inverse_product_qty_percentage', digits=(12, 3))
    product_actual_quantity = fields.Float(store=True, digits=(12, 3))

    # @api.depends('product_qty', 'bom_id.product_qty')
    # def _compute_product_actual_quantity(self):
    #     for line in self:
    #         if line.product_uom_id.is_kilogram:
    #             line.product_actual_quantity = line.bom_id.product_qty * line.product_qty_percentage * 1000
    #         else:
    #             line.product_actual_quantity = line.bom_id.product_qty * line.product_qty_percentage

    # def compute_actual_quantity(self):
    #     print('hello from')
    #     for rec in self:
    #         rec.product_actual_quantity = rec.product_qty

    @api.model
    def _get_default_product_qty(self):
        return self.default_get(['product_qty'])['product_qty']


    @api.depends('product_qty')
    def _compute_product_qty_percentage(self):
        for rec in self:
            if rec.bom_id.product_uom_id.is_tons:
                if rec.product_uom_id.is_kilogram:
                    rec.product_qty_percentage = rec.product_qty / 1000
                else:
                    rec.product_qty_percentage = rec.product_qty
            else:
                rec.product_qty_percentage = rec.product_qty

    @api.depends('product_qty_percentage')
    def _inverse_product_qty_percentage(self):
        for rec in self:
            if rec.bom_id.product_uom_id.is_tons:
                if rec.product_uom_id.is_kilogram:
                    rec.product_qty = rec.product_qty_percentage * 1000
                else:
                    rec.product_qty = rec.product_qty_percentage
            else:
                rec.product_qty = rec.product_qty_percentage
