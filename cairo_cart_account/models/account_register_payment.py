from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from collections import defaultdict


class AccountRegisterPaymentInherit(models.TransientModel):
    _inherit = "account.payment.register"

    account_move_id = fields.Many2one(comodel_name="account.move", string="", required=False,
                                      compute='compute_account_move_id')

    payment_method = fields.Many2one('account.payment.method.line', string='Payment Method')



    def compute_account_move_id(self):
        active_model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_ids')
        if active_model and active_id and len(active_id) == 1:
            self.account_move_id = self.env['account.move'].browse(active_id)
        else:
            self.account_move_id = False
        print('self.account_move_id', self.account_move_id)

    def action_create_payments(self):
        res = super(AccountRegisterPaymentInherit, self).action_create_payments()

        if self.payment_method_line_id and self.account_move_id:
            self.account_move_id.write({
                'payment_method': self.payment_method_line_id.id,
            })



        return res