# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResCompany(models.Model):
    _inherit = 'res.company'

    ol_max_discount = fields.Float('Max Discount')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ol_max_discount = fields.Float('Max Discount', related='company_id.ol_max_discount', readonly=False)


class PosSession(models.Model):
    _inherit = 'pos.session'

    def _loader_params_res_company(self):
        result = super()._loader_params_res_company()
        result['search_params']['fields'].append('ol_max_discount')
        return result
