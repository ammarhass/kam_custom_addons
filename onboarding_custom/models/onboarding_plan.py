from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class OnBoardingPlan(models.Model):
    _name = 'onboarding.plan'

    name = fields.Char()
    summary = fields.Text()
    hr_approval = fields.Boolean()
    employee_assign = fields.Boolean()
    department_id = fields.Many2one('hr.department')
    employee_id = fields.Many2one('hr.employee')

    @api.constrains('hr_approval')
    def _check_hr_approval_order(self):
        """Ensure HR approval order is maintained."""
        for record in self:
            if record.hr_approval:
                # Get all lines for the employee ordered by creation
                lines = record.employee_id.onboarding_ids
                for line in lines:
                    if line == record:
                        # Stop checking once we reach the current record
                        break
                    if not line.hr_approval and not self.env.user.has_group('onboarding_custom.group_onboarding_plan'):
                        raise ValidationError(_(
                            "You cannot approve this line because a previous line is not yet approved."
                        ))


