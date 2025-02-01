from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    purchase_total_quantity = fields.Float(compute='_compute_total_quantity')

    @api.depends('order_line')
    def _compute_total_quantity(self):
        self = self.sudo()
        for rec in self:
            if rec.order_line:
                rec.purchase_total_quantity = sum(rec.order_line.mapped('product_qty'))
            else:
                rec.purchase_total_quantity = 0.0

