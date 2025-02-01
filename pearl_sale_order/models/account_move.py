from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move'

    invoice_total_quantity = fields.Float(compute='_compute_total_quantity')

    @api.depends('invoice_line_ids')
    def _compute_total_quantity(self):
        self = self.sudo()
        for rec in self:
            if rec.invoice_line_ids:
                rec.invoice_total_quantity = sum(rec.invoice_line_ids.mapped('quantity'))
            else:
                rec.invoice_total_quantity = 0.0
