from collections import defaultdict

from odoo.exceptions import UserError
from odoo import models, fields, api, _


class InheritAccountMove(models.Model):
    _inherit = 'account.move'

    # state = fields.Selection([
    #     ('draft', 'Draft'),
    #     ('proforma', 'Pro-forma'),
    #     ('proforma2', 'Pro-forma'),
    #     ('posted', 'Posted'),
    #     ('post', 'Post'),
    #     ('cancel', 'Cancelled'),
    #     ('done', 'Received'),
    #     ('audit_pass', 'Audit Pass'),
    #     ('audit_not_pass', 'Audit Not Pass'),
    #     ('audit_accept', 'Audit Accepted')
    # ], string='Status', index=True, readonly=True, default='draft',
    #     track_visibility='onchange', copy=False)
    audit_note_ids = fields.Many2many('audit.note')

    audit_state = fields.Selection([
        ('audit_pass', 'Audit Pass'),
        ('audit_not_pass', 'Audit Not Pass'),
        ('audit_accept', 'Audit Accepted')
    ])

    @api.model_create_multi
    def create(self, vals_list):
        moves = super().create(vals_list)
        for move in moves:
            if move.stock_move_id:
                if move.stock_move_id.picking_id:
                    attachments = self.env['ir.attachment'].search([
                        ('res_model', '=', 'stock.picking'),
                        ('res_id', '=', move.stock_move_id.picking_id.id)
                    ])
                    for attachment in attachments:
                        attachment.copy({'res_model': 'account.move', 'res_id': move.id})
                elif move.stock_move_id.production_id:
                    attachments = self.env['ir.attachment'].search([
                        ('res_model', '=', 'mrp.production'),
                        ('res_id', '=', move.stock_move_id.production_id.id)
                    ])
                    for attachment in attachments:
                        attachment.copy({'res_model': 'account.move', 'res_id': move.id})
        return moves

    # def write(self, vals):
    #     # Check if journal_id is in vals
    #     if 'journal_id' in vals:
    #         journal_id = vals.pop('journal_id')
    #         # Update the journal_id directly in the database using SQL
    #         self.env.cr.execute("""
    #             UPDATE account_move
    #             SET journal_id = %s
    #             WHERE id IN %s
    #         """, (journal_id, tuple(self.ids)))
    # 
    #     # Proceed with the regular write process for other fields
    #     try:
    #         return super().write(vals)
    #     except exceptions.UserError as e:
    #         # Handle or log the exception if necessary
    #         raise e


    def audit_accept(self):
        self.audit_state = 'audit_accept'

    @api.depends('company_id', 'invoice_filter_type_domain')
    def _compute_suitable_journal_ids(self):
        for m in self:
            journal_type = m.invoice_filter_type_domain or []
            company_id = m.company_id.id or self.env.company.id
            domain = [('company_id', '=', company_id)]
            m.suitable_journal_ids = self.env['account.journal'].search(domain)

    def server_action_bulk_pass(self):
        for rec in self:
            rec.audit_state = 'audit_pass'

    def server_action_bulk_accept(self):
        for rec in self:
            rec.audit_state = 'audit_accept'

    # @api.depends('amount_residual', 'move_type', 'state', 'company_id')
    # def _compute_payment_state(self):
    #     stored_ids = tuple(self.ids)
    #     if stored_ids:
    #         self.env['account.partial.reconcile'].flush_model()
    #         self.env['account.payment'].flush_model(['is_matched'])
    #
    #         queries = []
    #         for source_field, counterpart_field in (('debit', 'credit'), ('credit', 'debit')):
    #             queries.append(f'''
    #                     SELECT
    #                         source_line.id AS source_line_id,
    #                         source_line.move_id AS source_move_id,
    #                         account.account_type AS source_line_account_type,
    #                         ARRAY_AGG(counterpart_move.move_type) AS counterpart_move_types,
    #                         COALESCE(BOOL_AND(COALESCE(pay.is_matched, FALSE))
    #                             FILTER (WHERE counterpart_move.payment_id IS NOT NULL), TRUE) AS all_payments_matched,
    #                         BOOL_OR(COALESCE(BOOL(pay.id), FALSE)) as has_payment,
    #                         BOOL_OR(COALESCE(BOOL(counterpart_move.statement_line_id), FALSE)) as has_st_line
    #                     FROM account_partial_reconcile part
    #                     JOIN account_move_line source_line ON source_line.id = part.{source_field}_move_id
    #                     JOIN account_account account ON account.id = source_line.account_id
    #                     JOIN account_move_line counterpart_line ON counterpart_line.id = part.{counterpart_field}_move_id
    #                     JOIN account_move counterpart_move ON counterpart_move.id = counterpart_line.move_id
    #                     LEFT JOIN account_payment pay ON pay.id = counterpart_move.payment_id
    #                     WHERE source_line.move_id IN %s AND counterpart_line.move_id != source_line.move_id
    #                     GROUP BY source_line_id, source_move_id, source_line_account_type
    #                 ''')
    #
    #         self._cr.execute(' UNION ALL '.join(queries), [stored_ids, stored_ids])
    #
    #         payment_data = defaultdict(lambda: [])
    #         for row in self._cr.dictfetchall():
    #             payment_data[row['source_move_id']].append(row)
    #     else:
    #         payment_data = {}
    #
    #     for invoice in self:
    #         if invoice.payment_state == 'invoicing_legacy':
    #             # invoicing_legacy state is set via SQL when setting setting field
    #             # invoicing_switch_threshold (defined in account_accountant).
    #             # The only way of going out of this state is through this setting,
    #             # so we don't recompute it here.
    #             continue
    #
    #         currencies = invoice._get_lines_onchange_currency().currency_id
    #         currency = currencies if len(currencies) == 1 else invoice.company_id.currency_id
    #         reconciliation_vals = payment_data.get(invoice.id, [])
    #         payment_state_matters = invoice.is_invoice(True)
    #
    #         # Restrict on 'receivable'/'payable' lines for invoices/expense entries.
    #         if payment_state_matters:
    #             reconciliation_vals = [x for x in reconciliation_vals if
    #                                    x['source_line_account_type'] in ('asset_receivable', 'liability_payable')]
    #
    #         new_pmt_state = 'not_paid'
    #         if invoice.state in ['posted', 'audit_pass', 'audit_accept']:
    #
    #             # Posted invoice/expense entry.
    #             if payment_state_matters:
    #
    #                 if currency.is_zero(invoice.amount_residual):
    #                     if any(x['has_payment'] or x['has_st_line'] for x in reconciliation_vals):
    #
    #                         # Check if the invoice/expense entry is fully paid or 'in_payment'.
    #                         if all(x['all_payments_matched'] for x in reconciliation_vals):
    #                             new_pmt_state = 'paid'
    #                         else:
    #                             new_pmt_state = invoice._get_invoice_in_payment_state()
    #
    #                     else:
    #                         new_pmt_state = 'paid'
    #
    #                         reverse_move_types = set()
    #                         for x in reconciliation_vals:
    #                             for move_type in x['counterpart_move_types']:
    #                                 reverse_move_types.add(move_type)
    #
    #                         in_reverse = (invoice.move_type in ('in_invoice', 'in_receipt')
    #                                       and (reverse_move_types == {'in_refund'} or reverse_move_types == {
    #                                     'in_refund', 'entry'}))
    #                         out_reverse = (invoice.move_type in ('out_invoice', 'out_receipt')
    #                                        and (reverse_move_types == {'out_refund'} or reverse_move_types == {
    #                                     'out_refund', 'entry'}))
    #                         misc_reverse = (invoice.move_type in ('entry', 'out_refund', 'in_refund')
    #                                         and reverse_move_types == {'entry'})
    #                         if in_reverse or out_reverse or misc_reverse:
    #                             new_pmt_state = 'reversed'
    #
    #                 elif reconciliation_vals:
    #                     new_pmt_state = 'partial'
    #
    #         invoice.payment_state = new_pmt_state
