from odoo import models, fields, api, _


class CustodyRequest(models.Model):
    _inherit = ['hr.custody.request']

    # is_first_approval = fields.Boolean(default=_compute_first_approval)
    # is_second_approval = fields.Boolean(default=_compute_second_approval)

    is_first_approval = fields.Boolean(
        compute='_compute_first_approval',
        store=False
    )
    is_second_approval = fields.Boolean(
        compute='_compute_second_approval',
        store=False
    )
    first_approval = fields.Many2one(related='employee_id.first_approval')
    second_approval = fields.Many2one(related='employee_id.second_approval')
    company_id = fields.Many2one(
        comodel_name="res.company", string="Company", index=1, default=lambda self: self.env.company
    )


    state = fields.Selection(string="", selection=[('draft', 'Draft'), ('first_approve', 'First Approve'), ('approved', 'Approved'), ('paid', 'Paid'),
                                                   ('settled', 'Settled'), ], required=False, default="draft")


    @api.model
    def create(self, vals):
        res = super().create(vals)
        mail_template = self.env.ref('custody_custom.send_first_approve_email')
        mail_template.send_mail(res.id, force_send=True, email_values={'res_id': res.id})
        return res

    def _compute_first_approval(self):
        """Compute if the current user is the first approver."""
        for rec in self:
            rec.is_first_approval = (
                rec.employee_id
                and rec.employee_id.first_approval
                and rec.employee_id.first_approval.id == self.env.user.employee_id.id
            )

    def _compute_second_approval(self):
        """Compute if the current user is the second approver."""
        for rec in self:
            rec.is_second_approval = (
                rec.employee_id
                and rec.employee_id.second_approval
                and rec.employee_id.second_approval.id == self.env.user.employee_id.id
            )

    def action_first_approve(self):
        self = self.sudo()
        for rec in self:
            rec.write({'state': 'first_approve'})
            if rec.requested_value <= rec.employee_id.first_amount_to:
                rec.set_approved()
            else:
                mail_template = self.env.ref('custody_custom.send_second_approve_email')
                mail_template.send_mail(rec.id, force_send=True, email_values={'res_id': rec.id})




