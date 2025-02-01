from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrAttendanceRule(models.Model):

    _inherit = 'hr.attendance.rule'

    employee_ids = fields.Many2many('hr.employee', 'hr_attendance_rule_id')
    hour_salary = fields.Boolean()
    number_of_minutes = fields.Float(default=1)
    approved_month_work_minutes = fields.Float()
    break_time = fields.Float(default=0.0)
    apply_break_time = fields.Boolean()


    @api.constrains('number_of_minutes')
    def number_of_minutes_fun(self):
        for rec in self:
            if rec.number_of_minutes == 0:
                raise ValidationError("Number Of Minutes must be greater than 0")

    @api.constrains('employee_ids')
    def _check_unique_employees(self):
        # Get all employee IDs in the current records
        print("hello")
        rules=self.env['hr.attendance.rule'].search([('id','!=',self.id),('employee_ids','in', self.employee_ids.ids)])
        if rules:
            raise ValidationError(_("Cannot Use Same Employee in Two Rules"))


class AttendanceRuleLine(models.Model):
    _inherit = 'hr.attendance.rule.line'

    early = fields.Boolean()
    late = fields.Boolean()
