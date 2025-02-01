from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.onchange("branch_id")
    def onchange_branch_id(self):
        print("hello")
        self.invoice_line_ids._compute_account_id()