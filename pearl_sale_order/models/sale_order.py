from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):

    _inherit = 'sale.order'

    partner_id = fields.Many2one(
        domain="[('type', '!=', 'private'), ('company_id', '=', company_id), ('is_customer', '=', True), ('active', '=', True), ('user_id', '=', uid)]",)

    sale_total_quantity = fields.Float(compute='_compute_total_quantity')

    phase_approval = fields.Selection([
        ('first', 'First Approval'),
        ('second', 'Second Approval'),
        ('third', 'Third Approval')
    ])

    customer_address = fields.Text()

    # @api.constrains('order_line')
    # def _constrain_product_quantity(self):
    #     for rec in self:
    #         for order in rec.order_line:
    #             if order.product_uom_qty > order.product_id.qty_available:
    #                 raise ValidationError("Please add an attachment to the record")
    #                 # raise ValidationError(_('The available Quantity of product ({}) is {}'.format(rec.product_id.name, rec.product_id.qty_available)))

    @api.depends('order_line')
    def _compute_total_quantity(self):
        self = self.sudo()
        for rec in self:
            if rec.order_line:
                rec.sale_total_quantity = sum(rec.order_line.mapped('product_uom_qty'))
            else:
                rec.sale_total_quantity = 0.0


    def first_phase_approval(self):
        for rec in self:
            rec._validate_tier()
        for rec in self:
            rec.with_context(skip_validation_check=True).write({'phase_approval': 'first'})

    def second_phase_approval(self):
        for rec in self:
            rec._validate_tier()
        for rec in self:
            rec.with_context(skip_validation_check=True).write({'phase_approval': 'second'})


    def third_phase_approval(self):
        for rec in self:
            rec._validate_tier()
        for rec in self:
            rec.action_confirm()
            rec.with_context(skip_validation_check=True).write({'phase_approval': 'third'})
