from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    property_account_receivable_id = fields.Many2one(
        'account.account',
        string="Account Receivable",
        domain="[('account_type', '=', 'asset_receivable'), ('deprecated', '=', False), ('company_id', '=', current_company_id)]",
        help="This account will be used instead of the default one as the receivable account for the current partner",
        required=True,
        default=lambda self: self._get_default_receivable_account()
    )
    property_account_payable_id = fields.Many2one('account.account',
                                                  string="Account Payable",
                                                  domain="[('account_type', '=', 'liability_payable'), ('deprecated', '=', False), ('company_id', '=', current_company_id)]",
                                                  help="This account will be used instead of the default one as the payable account for the current partner",
                                                  required=True,
                                                  default=lambda self: self._get_default_payable_account())

    def _get_default_receivable_account(self):
        # Fetch the first valid 'account.account' for the current company
        if self.env.company.is_gadara:
            account = self.env['account.account'].search([
                ('account_type', '=', 'asset_receivable'),
                ('deprecated', '=', False),
            ], limit=1)

        return account.id if account else False
    def _get_default_payable_account(self):
        # Fetch the first valid 'account.account' for the current company
        if self.env.company.is_gadara:
            account = self.env['account.account'].search([
                ('account_type', '=', 'liability_payable'),
                ('deprecated', '=', False),
            ], limit=1)

            return account.id if account else False
