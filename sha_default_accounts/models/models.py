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

    # delete_allowed = fields.Boolean(compute='_set_delete_allowed')
    #
    # @api.depends_context('uid')
    # def _set_delete_allowed(self):
    #     for rec in self:
    #         if self.env.user.has_group('point_of_sale.group_pos_manager'):
    #             rec.delete_allowed = True
    #         else:
    #             rec.delete_allowed = False
