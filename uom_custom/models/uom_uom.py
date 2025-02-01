from odoo import models, fields, api


class InheritUomUom(models.Model):
    _inherit = 'uom.uom'

    is_kilogram = fields.Boolean()
    is_tons = fields.Boolean()
    is_gram = fields.Boolean()