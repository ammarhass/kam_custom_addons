# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosConfig(models.Model):
    _inherit = 'pos.config'

    delete_allowed = fields.Boolean(compute='_set_delete_allowed')

    @api.depends_context('uid')
    def _set_delete_allowed(self):
        for rec in self:
            if self.env.user.has_group('point_of_sale.group_pos_manager'):
                rec.delete_allowed = True
            else:
                rec.delete_allowed = False
