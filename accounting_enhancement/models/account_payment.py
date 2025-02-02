from odoo import models, fields, api, tools, _
from odoo.exceptions import MissingError, ValidationError, AccessError

class AccountPaymentInherit(models.Model):
    _inherit = 'account.payment'

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self._context.get('default_payment_type') == 'outbound':
            return {
                'domain': {
                    'partner_id': [('supplier_rank', '>', 0)]
                }
            }
        else:
            # records = self.env['res.partner'].search(
            #     [('type', '!=', 'private'), ('is_customer', '=', True), ('active', '=', True),
            #      ('company_id', '!=', False)])
            # print("hello")
            return {
                'domain': {
                    'partner_id': [('customer_rank', '>', 0)]
                }
            }
