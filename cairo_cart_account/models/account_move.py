from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    downpayment_amount = fields.Monetary(
        compute='_compute_downpayment_amount',
        currency_field='currency_id',
        store=False
    )
    payment_move_ids = fields.One2many(
        'account.payment',  # Adjust the model name if necessary
        compute='_compute_payment_ids',
        string='Payments',
        readonly=True
    )
    payment_method = fields.Many2one('account.payment.method.line', string='Payment Method')



    @api.depends('payment_ids.amount')  # Assuming payment_ids is a One2many to payments
    def _compute_downpayment_amount(self):
        for record in self:
            record.downpayment_amount = sum(record.payment_move_ids.mapped('amount'))


    def _compute_payment_ids(self):
        for move in self:
            if move.state == 'draft':
                move.payment_move_ids = False
            else:
                print(move.name)
                    # Assuming 'partner_id' is the field linking partners in account.move
                payments = self.env['account.payment'].search([
                    ('ref', '=', move.name),
                    ('state', '=', 'posted'),

                    # ('matched_credit_ids', '=', True ),
                    # ('matched_debit_ids', '=', True ),

                ])
                print('payments', payments)

                move.payment_move_ids = [(6, 0, payments.ids)]

    # @api.depends('amount_total', 'currency_id', 'partner_id')
    # def _compute_downpayment_amount(self):
    #     for move in self:
    #         downpayment = 0.0
    #         if move.move_type == 'out_invoice':  # Ensure it's a customer invoice
    #             downpayment = move._get_downpayment_amount()
    #         move.downpayment_amount = downpayment
    #
    # def _get_downpayment_amount(self):
    #     """Calculate the downpayment amount from previous payments."""
    #     downpayment = 0.0
    #     payments = self.env['account.payment'].search([
    #         ('partner_id', '=', self.partner_id.id),
    #         ('state', '=', 'posted'),
    #         ('payment_type', '=', 'inbound'),  # Customer payment
    #         ('id', 'in', self.payment_ids.ids),
    #     ])
    #
    #     for payment in payments:
    #         if payment.reconciled_invoice_ids:
    #             for invoice in payment.reconciled_invoice_ids:
    #                 if invoice.id == self.id:
    #                     downpayment += payment.amount
    #
    #     return downpayment