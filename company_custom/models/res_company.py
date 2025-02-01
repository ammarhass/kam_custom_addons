from odoo import models, fields, api


class InheritResCompany(models.Model):
    _inherit = 'res.company'

    journal_entry = fields.Boolean()
    sales_invoice = fields.Boolean()
    vendor_bill = fields.Boolean()
    manufacturing_order = fields.Boolean()
    external_transfer = fields.Boolean()
    elazz_comp = fields.Boolean()