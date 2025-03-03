from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    tax_amount = fields.Monetary(
        compute="_compute_tax_amount",
        currency_field='currency_id',
        store=True
    )
    total_after_tax = fields.Monetary(
        compute="_compute_total_after_tax",
        currency_field='currency_id',
        store=False
    )

    @api.depends('tax_amount', 'price_subtotal')
    def _compute_total_after_tax(self):
        for rec in self:
            rec.total_after_tax = rec.price_subtotal + rec.tax_amount

    @api.depends('tax_ids', 'price_subtotal', 'move_id.currency_id')
    def _compute_tax_amount(self):
        for line in self:
            taxes = line.tax_ids.compute_all(
                line.price_subtotal,
                currency=line.move_id.currency_id,
                quantity=1.0,
                product=line.product_id,
                partner=line.move_id.partner_id
            )
            line.tax_amount = sum(t['amount'] for t in taxes['taxes']) if taxes else 0.0
