from odoo import models, fields, api

class HrRequest(models.Model):
    _name = "hr.request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "HR Request"

    name = fields.Char(compute='_compute_name',
                       help="Auto-generated field based on record's ID")
    request_type = fields.Selection([
        ('hr_letter', 'HR Letter'),
        ('embassy_letter', 'Embassy Letter'),
        ('experience_letter', 'Experience Letter')], string='Request Type',
        copy=False, default='hr_letter', required=True,
        help="Type of HR Request")
    employee_id = fields.Many2one('hr.employee', string='Employee', default=lambda self: self.env.user.employee_id,
                                       required=True,
                                       help="Employee requesting the equipment")
    department_id = fields.Many2one('hr.department', string='Department', default=lambda self: self.env.user.employee_id.department_id,
                                         help="Department of the employee")
    job_position_id = fields.Many2one('hr.job', string='Job Position', default=lambda self: self.env.user.employee_id.job_id,
                                      help="Job position of the employee")
    user_id = fields.Many2one('res.users', string='User',
                                    default=lambda self: self.env.user,
                                    help="User who created the equipment "
                                         "request")
    created_user_id = fields.Many2one('res.users', string='Created By',
                                      default=lambda self: self.env.user,
                                      help="User who created the equipment "
                                           "request")
    create_date = fields.Date(string='Created Date',
                              help="Date when the hr "
                                   "request was created")
    hr_user_id = fields.Many2one('res.users', string='HR Manager',
                                 help="HR Manager who approves the hr "
                                      "request")
    hr_date = fields.Date(string='HR Approved Date',
                          help="Date when the HR Manager approved the hr"
                               "request")

    company_id = fields.Many2one('res.company', string='Company',
                                      default=lambda self: self.env.company,
                                      help="Company of the employee")

    status = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'Waiting for Approval of HR'),
        ('approved', 'Approved'),
        ('ready', 'Ready To Collect'),
        ('reject', 'Rejected')],
        string='State', copy=False, default='draft', tracking=True,
        help="Status of the hr request")


    @api.depends('request_type', 'employee_id')
    def _compute_name(self):
        """ _rec_name = Employee Name + Request Type + Creation Date"""
        for record in self:
            record.name = str(record.employee_id.name) + ' - ' + str(
                record.request_type) + ' - ' + str(
                fields.date.today())

    def action_confirm(self):
        """Confirm Button"""
        self = self.sudo()
        self.write({'status': 'in_progress'})
        users = self.env.ref("hr_requests.group_hr_request_officer").users
        for user in users:
            self.activity_schedule(
                'mail.mail_activity_data_todo',
                user_id=user.id,
                summary="Please Check the HR Request",
            )

    def action_reject(self):
        """Reject Button"""
        self.write({'status': 'reject'})


    def action_approval_hr(self):
        """HR Approval Button also write the user who Approved this button
        and Date he approved"""
        self.write({'status': 'approved', 'hr_user_id': self.env.user.id,
                    'hr_date': fields.Date.today()})

    def action_ready(self):
        """ready Button"""
        self.write({'status': 'ready'})




