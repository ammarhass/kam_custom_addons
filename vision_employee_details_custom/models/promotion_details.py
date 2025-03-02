from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class PromotionDetails(models.Model):
    _name = 'promotion.details'

    job_id = fields.Many2one('hr.job')
    salary = fields.Monetary()
    employee_id = fields.Many2one('hr.employee')
    currency_id = fields.Many2one(
        'res.currency', string='Currency', required=True,
        default=lambda self: self.env.user.company_id.currency_id.id)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    promotion_details_ids = fields.One2many('promotion.details', 'employee_id')

    @api.onchange('job_id')
    def _onchange_job_fun(self):
        self.promotion_details_ids = [(0, 0, {
            'job_id': self.job_id.id,
            'salary': self.contract_id.wage
        })]