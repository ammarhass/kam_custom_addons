from odoo import models, fields, api
from odoo.exceptions import ValidationError


class InheritMrpUnbuild(models.Model):
    _inherit = 'mrp.unbuild'

    # bom_line_ids = fields.One2many('mrp.bom.line', 'unbuild_order_id', related='bom_id.bom_line_ids', readonly=False)
    unbuild_line_ids = fields.One2many('mrp.unbuild.line', 'unbuild_id', string="Unbuild BOM Lines")
    unbuild_order_percentage = fields.Boolean()
    product_qty = fields.Float(
        'Quantity', default=1.0,
        required=True, digits=(12, 3), states={'done': [('readonly', True)]})


    @api.onchange('product_qty', 'unbuild_line_ids', 'unbuild_line_ids.product_qty_percentage')
    def onchange_product_qty(self):
        for line in self.unbuild_line_ids:
            if line.product_uom_id.is_kilogram:
                line.product_actual_quantity = self.product_qty * line.product_qty_percentage * 1000
            else:
                line.product_actual_quantity = self.product_qty * line.product_qty_percentage


    @api.onchange('bom_id', 'product_qty')
    def _onchange_bom_id(self):
        """Update the unbuild_line_ids based on the selected bom_id and product_qty."""
        if self.bom_id:
            unbuild_lines = []
            for line in self.bom_id.bom_line_ids:
                # Adjust the quantities based on the unbuild order's product_qty
                if line.product_uom_id.is_kilogram:
                    product_actual_qty = self.product_qty * line.product_qty_percentage * 1000
                else:
                    product_actual_qty = self.product_qty * line.product_qty_percentage

                unbuild_lines.append((0, 0, {
                    'product_id': line.product_id.id,
                    'product_uom_id': line.product_uom_id.id,
                    'product_qty_percentage': line.product_qty_percentage,
                    'product_actual_quantity': product_actual_qty,
                }))
            if not self.unbuild_line_ids:
                self.unbuild_line_ids = unbuild_lines

    def write(self, vals):
        """Ensure that updates to bom_id or product_qty properly reflect in unbuild_line_ids."""
        res = super(InheritMrpUnbuild, self).write(vals)
        if 'bom_id' in vals or 'product_qty' in vals:
            self._onchange_bom_id()
        return res

    @api.model_create_multi
    def create(self, vals):
        unbuilds = super(InheritMrpUnbuild, self).create(vals)
        for unbuild in unbuilds:
            for line in unbuild['unbuild_line_ids']:
                if line.product_uom_id.is_kilogram:
                    line.write({'product_actual_quantity': unbuild['product_qty'] * line.product_qty_percentage * 1000})
                else:
                    line.write({'product_actual_quantity': unbuild['product_qty'] * line.product_qty_percentage})
        return unbuilds

    def action_validate(self):
        for rec in self:
            for line in rec.unbuild_line_ids:
                record = rec.bom_id.bom_line_ids.filtered(lambda x: x.product_id.id == line.product_id.id)
                if record:
                    record.product_qty_percentage = line.product_qty_percentage
        return super().action_validate()

    @api.constrains('bom_line_ids')
    def _check_bom_line_qty(self):
        for bom in self:
            # total_qty = sum(bom.bom_line_ids.mapped('product_qty'))
            # if total_qty > bom.product_qty:
            #     raise ValidationError('The total quantity of BoM lines must not be great than the BoM product quantity.')
            if bom.product_uom_id.category_id.is_weight:
                total_qty = 0.0
                for line in bom.bom_line_ids:
                    if line.product_uom_id.is_tons:
                        total_qty += line.product_actual_quantity * 1000
                    else:
                        total_qty += line.product_actual_quantity

                if bom.product_uom_id.is_kilogram:
                    if total_qty > bom.product_qty:
                        raise ValidationError('The total quantity of BoM lines must not be great than the BoM product quantity.')
                elif bom.product_uom_id.is_tons:
                    if total_qty > bom.product_qty * 1000:
                        raise ValidationError('The total quantity of BoM lines must not be great than the BoM product quantity.')


class MrpUnbuildLine(models.Model):
    _name = 'mrp.unbuild.line'
    _description = 'Unbuild BoM Line'

    unbuild_id = fields.Many2one('mrp.unbuild', string="Unbuild Order", required=True, ondelete="cascade")
    product_id = fields.Many2one('product.product', string="Product", required=True)
    product_uom_id = fields.Many2one('uom.uom', string="Unit of Measure", required=True)
    product_qty_percentage = fields.Float('Quantity', required=True, digits=(12, 3))
    product_actual_quantity = fields.Float('Actual Quantity', required=True, digits=(12, 3))
