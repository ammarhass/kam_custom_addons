from odoo import models, fields, api


class InheritAccountPayment(models.Model):
    _inherit = 'account.payment'
    partner_id = fields.Many2one(
        domain="[]",
    )

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_type == 'supplier':
            return {
                'domain': {
                    'partner_id':[('active', '=', True),('company_id', '!=', False),('is_vendor', '=', True)]
                }
            }
        elif self.partner_type == 'customer':
            return {
                'domain': {
                    'partner_id': [('active', '=', True),('company_id', '!=', False),('is_customer', '=', True)]
                }
            }


