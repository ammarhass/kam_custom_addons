from odoo import models, fields, api


class InheritPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    fraction_value = fields.Float()
    net_value = fields.Float()
    white_rice_quantity = fields.Float(compute='_compute_white_rice_quantity')
    fraction_quantity = fields.Float(compute='_compute_fraction_quantity')
    good_rice_quantity = fields.Float(compute='_compute_good_rice_quantity')

    @api.model_create_multi
    def create(self, vals_list):
        sellers = super().create(vals_list)
        return sellers

    # @api.depends('product_id')
    # def _compute_net_value(self):
    #     for rec in self:
    #         if rec.product_id.seller_ids.filtered(lambda x: x.partner_id == rec.order_id.partner_id):
    #             rec.net_value = rec.product_id.seller_ids.filtered(lambda x: x.partner_id == rec.order_id.partner_id).net_value
    #         else:
    #             rec.net_value = rec.net_value
    #
    # @api.depends('product_id')
    # def _compute_fraction_value(self):
    #     for rec in self:
    #         if rec.product_id.seller_ids.filtered(lambda x: x.partner_id == rec.order_id.partner_id):
    #             rec.fraction_value = rec.product_id.seller_ids.filtered(lambda x: x.partner_id == rec.order_id.partner_id).fraction_value
    #         else:
    #             rec.fraction_value = rec.net_value

    @api.depends('net_value', 'product_qty')
    def _compute_white_rice_quantity(self):
        for rec in self:
            rec.white_rice_quantity = rec.product_qty * rec.net_value

    @api.depends('fraction_value', 'white_rice_quantity')
    def _compute_fraction_quantity(self):
        for rec in self:
            rec.fraction_quantity = rec.white_rice_quantity * rec.fraction_value

    @api.depends('white_rice_quantity', 'fraction_quantity')
    def _compute_good_rice_quantity(self):
        for rec in self:
            rec.good_rice_quantity = rec.white_rice_quantity - rec.fraction_quantity