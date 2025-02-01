from odoo import models, fields, api
from datetime import datetime, date


class PayrollActivity(models.Model):
    _name = 'payroll.activity'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = 'name'

    name = fields.Char()
    date = fields.Date()
    assigned_to = fields.Many2many('res.users')
    message = fields.Text()

    def _payroll_activity_alarm(self):
        records = self.env['payroll.activity'].search([])
        for record in records:
            if record.date == date.today():
                for user in record.assigned_to:
                    todos = {
                        'res_id': record.id,
                        'res_model_id': self.env['ir.model'].search([('model', '=', 'payroll.activity')]).id,
                        'user_id': user.id,
                        'summary': 'Payroll Time',
                        'activity_type_id': 1,
                        # 'date_deadline': datetime.date.today(),
                    }
                    self.env['mail.activity'].create(todos)