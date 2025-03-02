# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosConfig(models.Model):
    _inherit = 'pos.config'

    default_account_receivable_id = fields.Many2one('account.account', company_dependent=True, string="Account Receivable",
                                                    domain="[('account_type', '=', 'asset_receivable'), ('deprecated', '=', False), "
                                                           "('company_id', '=', current_company_id)]")

    default_account_payable_id = fields.Many2one('account.account', company_dependent=True, string="Account Payable",
                                                 domain="[('account_type', '=', 'liability_payable'), ('deprecated', '=', False), "
                                                        "('company_id', '=', current_company_id)]")


class PosOrder(models.Model):
    _inherit = 'pos.order'

    phone = fields.Char(related='partner_id.phone')
