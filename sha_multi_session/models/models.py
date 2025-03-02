# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class PosConfig(models.Model):
    _inherit = 'pos.config'

    def _action_to_open_ui(self):
        if not self.current_session_id:
            old_session = self.env['pos.session'].sudo().search([('user_id', '=', self.env.user.id), ('state', 'in', ('opened', 'opening_control'))])
            if old_session:
                raise ValidationError(_(f"Session ( {old_session.mapped('name')} ) already opened."))
            self.env['pos.session'].create({'user_id': self.env.uid, 'config_id': self.id})
        path = '/pos/web' if self._force_http() else '/pos/ui'
        return {
            'type': 'ir.actions.act_url',
            'url': path + '?config_id=%d' % self.id,
            'target': 'self',
        }
