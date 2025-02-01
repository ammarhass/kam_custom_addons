from odoo import models, fields, api


class InheritPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    vendor_type = fields.Selection(selection=[('local', 'Local Vendor'),
                                              ('international', 'International Vendor')])
