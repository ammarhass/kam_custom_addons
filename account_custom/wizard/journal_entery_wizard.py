from odoo import models, fields, api


class JournalEntryWizard(models.TransientModel):
    _name = 'journal.entry.wizard'

    audit_result = fields.Selection([
        ('pass', 'Pass'),
        ('not_pass', 'Not Pass')
    ])
    # audit_note = fields.Text()
    journal_id = fields.Many2one('account.move')
    audit_note_ids = fields.Many2many('audit.note')

    def audit_submit(self):
        active_id = self.env.context.get('active_id')
        move = self.env['account.move'].browse(active_id)
        if move:
            if self.audit_result == 'pass':
                # move.write({'state': 'audit_pass'})
                move.audit_state = 'audit_pass'
            elif self.audit_result == 'not_pass':
                move.audit_state = 'audit_not_pass'
                move.write({'audit_note_ids': self.audit_note_ids})
        return {'type': 'ir.actions.act_window_close'}
