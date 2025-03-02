# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountAccountInherit(models.Model):
    _inherit = "account.account"

    is_dashboard = fields.Boolean(string="Dashboard",  )
    current_balance_Stored = fields.Float(string='Current Balance', compute='compute_current_balance_Stored',
                                          store=True)

    @api.depends('current_balance')
    def compute_current_balance_Stored(self):
        for rec in self:
            if rec.current_balance:
                rec.current_balance_Stored = rec.current_balance
            else:
                rec.current_balance_Stored = 0

    @api.model
    def get_total_current_balance(self):
        """Compute the total current_balance for all accounts with is_dashboard = True."""
        accounts = self.search([])
        total_balance = sum(accounts.mapped('current_balance'))
        return total_balance

    @api.model
    def get_total_positive_balance(self):
        """Compute the total current_balance for all accounts with is_dashboard = True, considering only positive balances."""
        accounts = self.search([])
        # Filter positive current_balance values
        positive_balances = accounts.mapped('current_balance') if not accounts else []
        positive_balances = [balance for balance in positive_balances if balance > 0]
        total_balance = sum(positive_balances)
        return total_balance