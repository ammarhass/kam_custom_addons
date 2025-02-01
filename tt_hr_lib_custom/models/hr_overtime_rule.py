from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrOverTimeRule(models.Model):

    _inherit = 'hr.overtime.rule'

    employee_ids = fields.Many2many('hr.employee')

    @api.constrains('employee_ids')
    def _check_unique_employees(self):
        # Get all employee IDs in the current records
        print("hello")
        rules=self.env['hr.attendance.rule'].search([('id','!=',self.id),('employee_ids','in', self.employee_ids.ids)])
        if rules:
            raise ValidationError(_("Cannot Use Same Employee in Two Rules"))