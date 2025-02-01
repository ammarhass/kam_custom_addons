from odoo import models, fields, api


class InheritAccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    mandatory_partner = fields.Boolean(related='account_id.mandatory_partner')
    mandatory_analytic_account = fields.Boolean(related='account_id.mandatory_analytic_account')
    product_weight = fields.Float('Product Weight')

