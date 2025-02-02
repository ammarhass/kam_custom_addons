from odoo import models, fields, api, tools, _
from odoo.exceptions import MissingError, ValidationError, AccessError

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    # vendor_partner_id = fields.Many2one(
    #     comodel_name='res.partner',
    #     string='Vendor',domain="[('supplier_rank', '>', 0)]",
    #
    # )
    # partner_id = fields.Many2one(
    #     'res.partner',
    #     string='Partner',
    #     readonly=True,
    #     tracking=True,
    #     strore=True,
    #     states={'draft': [('readonly', False)]},
    #     inverse='_inverse_partner_id',
    #     related='vendor_partner_id',
    #     compute_sudo=True,
    #     check_company=True,
    #     change_default=True,
    #     index=True,
    #     ondelete='restrict',
    # )

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self._context.get('default_move_type') in ('in_invoice','in_refund','in_receipt'):
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







