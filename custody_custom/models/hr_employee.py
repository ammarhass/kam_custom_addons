from odoo import models, fields, api, _

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    first_approval = fields.Many2one('hr.employee')
    first_amount_from = fields.Monetary()
    first_amount_to = fields.Monetary()
    second_approval = fields.Many2one('hr.employee')
    second_amount_from = fields.Monetary()
    second_amount_to = fields.Monetary()
