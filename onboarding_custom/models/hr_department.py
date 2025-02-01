from odoo import models, fields, api, _

class HrDepartment(models.Model):
    _inherit = 'hr.department'

    onboarding_ids = fields.One2many('onboarding.plan', 'department_id')
