from odoo import models, fields, api

class AccountAccount(models.Model):
    _inherit = 'account.account'

    remove_from_report = fields.Boolean()
