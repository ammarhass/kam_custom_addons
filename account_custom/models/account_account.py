from odoo import models, fields, api


class InheritAccountAccount(models.Model):
    _inherit = 'account.account'

    mandatory_partner = fields.Boolean()
    mandatory_analytic_account = fields.Boolean()