from odoo import api, fields, models, _
from odoo.exceptions import UserError

class ImportResPartner(models.Model):
    _inherit = 'res.partner'

    is_contact = fields.Boolean()
    is_customer = fields.Boolean()
    is_vendor = fields.Boolean()
    is_employee = fields.Boolean()
    company_id = fields.Many2one('res.company', 'Company', index=True, default=lambda self: self.env.company)

    @api.model
    def create(self, vals_list):
        res = super().create(vals_list)
        if self._context.get('res_partner_search_mode') == 'supplier':
            res.write({'is_vendor': True})
        elif self._context.get('res_partner_search_mode') == 'customer':
            res.write({'is_customer': True})
        else:
            res.write({'is_contact': True})
        return res

    def write(self, vals):
        res = super().write(vals)
        print('hello')
        return res

    @api.ondelete(at_uninstall=False)
    def _unlink_except_active_pos_session(self):
        running_sessions = self.env['pos.session'].sudo().search([('state', '!=', 'closed'), ('company_id', '=', self.env.company.id)])
        if running_sessions:
            raise UserError(
                _("You cannot delete contacts while there are active PoS sessions. Close the session(s) %s first.")
                % ", ".join(session.name for session in running_sessions)
            )




class AccountMove(models.Model):
        _inherit = 'account.move'

        # partner_id = fields.Many2one('res.partner', string="Partner")
        company_id = fields.Many2one(
            comodel_name='res.company',
            required=True, index=True,
            default=lambda self: self.env.company)


        @api.onchange('partner_id')
        def _onchange_partner_id(self):
            if self._context.get('default_move_type') == 'in_invoice':
                return {
                    'domain': {
                        'partner_id': [('type', '!=', 'private'), ('is_vendor', '=', True), ('active', '=', True), ('company_id', '!=', False)]
                    }
                }
            else:
                return {
                    'domain': {
                        'partner_id': [('type', '!=', 'private'), ('is_customer', '=', True), ('active', '=', True), ('company_id', '!=', False)]
                    }
                }

            # return {}
