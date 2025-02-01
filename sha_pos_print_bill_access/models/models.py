# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PosOrder(models.Model):
    _inherit = 'pos.order'

    is_printed = fields.Boolean(default=False, copy=False)

    def set_table_is_printed(self, ref):
        # print("set_table_is_printed")
        order_id = self.search([('pos_reference', '=', ref)])
        # print("order_id: ", order_id)
        order_id.is_printed = True
