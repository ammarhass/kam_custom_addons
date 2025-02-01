from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    num_of_days = fields.Integer("Number Of Days")