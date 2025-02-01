from odoo import models, fields, api


class InheritUomCategory(models.Model):
    _inherit = 'uom.category'

    is_weight = fields.Boolean()