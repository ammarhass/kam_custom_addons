from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PosSessionInherit(models.Model):
    _inherit = 'pos.session'

    def _get_pos_ui_res_users(self, params):
        user = self.env['res.users'].search_read(**params['search_params'], limit=1)
        if not user:
            raise UserError(_("You do not have permission to open a POS session. Please try opening a session with a different user"))
        user = user[0]
        sub_id = self.env.ref("sha_pos_custom_receipt.group_sub_admin")
        # user['role'] = 'manager' if any(id == self.config_id.group_pos_manager_id.id for id in user['groups_id']) else 'cashier'
        user['role'] = 'manager' if any(id in [self.config_id.group_pos_manager_id.id, sub_id.id] for id in user['groups_id']) else 'cashier'
        del user['groups_id']
        return user
