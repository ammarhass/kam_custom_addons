from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountMove(models.Model):

    _inherit = 'account.move'

    analytic_account_id = fields.Many2one('account.analytic.account')
    is_item_expenses = fields.Boolean()

    @api.constrains('analytic_account_id')
    def _analytic_account_constrain(self):
        allowed_group = self.env.ref('arkad_excel_report.arkad_normal_group')
        admin_group = self.env.ref('base.group_erp_manager')
        for rec in self:
             if allowed_group in self.env.user.groups_id and admin_group not in self.env.user.groups_id:
                 if not rec.analytic_account_id:
                     raise ValidationError(_('Please add an analytic account'))

    @api.constrains('partner_id')
    def _partner_id_constrain(self):
        allowed_group = self.env.ref('arkad_excel_report.arkad_normal_group')
        admin_group = self.env.ref('base.group_erp_manager')
        for rec in self:
             if allowed_group in self.env.user.groups_id and admin_group not in self.env.user.groups_id:
                 if not rec.partner_id:
                     raise ValidationError(_('Please add vendor/customer'))


    @api.onchange('analytic_account_id')
    def _onchange_analytic_account_id(self):
        if self.analytic_account_id:
            account_id = self.analytic_account_id
            for line in self.invoice_line_ids:
                line.analytic_distribution = {str(account_id.id): 100.00}

    @api.onchange('invoice_line_ids')
    def _onchange_Line_analytic_account_id(self):
        if self.analytic_account_id:
            account_id = self.analytic_account_id
            for line in self.invoice_line_ids:
                line.analytic_distribution = {str(account_id.id): 100.00}
