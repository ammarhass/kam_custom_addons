from odoo import models, fields, api, _

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    first_approval = fields.Many2one('hr.employee')
    first_amount_from = fields.Monetary()
    first_amount_to = fields.Monetary()
    second_approval = fields.Many2one('hr.employee')
    second_amount_from = fields.Monetary()
    second_amount_to = fields.Monetary()
    third_approval = fields.Many2one('hr.employee')
    third_amount_from = fields.Monetary()
    third_amount_to = fields.Monetary()
    fourth_approval = fields.Many2one('hr.employee')
    fourth_amount_from = fields.Monetary()
    fourth_amount_to = fields.Monetary()
