from odoo import models, fields, api


class InheritProductSupplierInfo(models.Model):
    _inherit = 'product.supplierinfo'

    fraction_value = fields.Float()
    net_value = fields.Float()
    white_rice_quantity = fields.Float(compute='_compute_white_rice_quantity')
    fraction_quantity = fields.Float(compute='_compute_fraction_quantity')
    good_rice_quantity = fields.Float(compute='_compute_good_rice_quantity')
    date = fields.Date()
    min_qty = fields.Float(
        'Quantity', default=0.0, required=True, digits=(12, 3),
        help="The quantity to purchase from this vendor to benefit from the price, expressed in the vendor Product Unit of Measure if not any, in the default unit of measure of the product otherwise.")


    @api.model_create_multi
    def create(self, vals):
        sellers = super().create(vals)
        return sellers

    @api.depends('net_value', 'min_qty')
    def _compute_white_rice_quantity(self):
        for rec in self:
            rec.white_rice_quantity = rec.min_qty * rec.net_value

    @api.depends('fraction_value', 'white_rice_quantity')
    def _compute_fraction_quantity(self):
        for rec in self:
            rec.fraction_quantity = rec.white_rice_quantity * rec.fraction_value

    @api.depends('white_rice_quantity', 'fraction_quantity')
    def _compute_good_rice_quantity(self):
        for rec in self:
            rec.good_rice_quantity = rec.white_rice_quantity - rec.fraction_quantity



