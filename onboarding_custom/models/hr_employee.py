from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrEmployee(models.Model):
    _inherit = 'hr.employee'


    onboarding_ids = fields.One2many('onboarding.plan', 'employee_id')

    # @api.depends('department_id')
    # def _get_onboarding_ids(self):
    #     self = self.sudo()
    #     for record in self:
    #         department = record.department_id
    #         if not department or not department.onboarding_ids:
    #             record.onboarding_ids = False
    #         else:
    #             record.onboarding_ids = [
    #                 (0, 0, {
    #                     'name': line.name,
    #                     'summary': line.summary,
    #                 }) for line in department.onboarding_ids
    #             ]



    @api.onchange('department_id')
    def _onchange_department_id(self):
        """Copy onboarding plans from the selected department to the employee."""
        if self.department_id and not self.onboarding_ids:
            self.onboarding_ids = [
                (0, 0, {
                    'name': plan.name,
                    'summary': plan.summary,
                }) for plan in self.department_id.onboarding_ids
            ]
        else:
            self.onboarding_ids = []


