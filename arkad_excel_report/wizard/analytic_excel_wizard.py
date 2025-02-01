from odoo import models, fields, api

class Analytic_Wizard(models.TransientModel):

    _name = 'analytic.account.wizard'

    analytic_account_id = fields.Many2one('account.analytic.account')
    account_id = fields.Many2one('account.account')


    def account_fun(self):
        account_id = self.account_id.id  # Get the selected account_id from the wizard
        return {
            'type': 'ir.actions.act_url',
            'url': f'/analytic/excel/account/{self.env.context.get("active_ids")}?account_id={account_id}',
            'target': 'new'
        }



