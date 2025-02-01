# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class AccountInvoiceReport(models.Model):
    _inherit = 'account.invoice.report'

    brand_id = fields.Many2one(comodel_name='product.brand', string="Brand", readonly=True)

    # def _select(self):
    #     return super()._select() + ", line.brand_id as brand_id"