from odoo import models, fields, api


class AnalyticAccount(models.Model):

    _inherit ='account.analytic.account'


    def create_analytic_report(self):
        return {
            'type': 'ir.actions.act_url',
            'url': f'/analytic/excel/report/{self.env.context.get("active_ids")}',
            'target': 'new'
        }

    def create_analytic_report_vendor(self):
        return {
            'type': 'ir.actions.act_url',
            'url': f'/analytic/excel/report/vendor/{self.env.context.get("active_ids")}',
            'target': 'new'
        }