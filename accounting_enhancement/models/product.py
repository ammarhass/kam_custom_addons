from odoo import models, fields, api, tools, _
from odoo.exceptions import MissingError, ValidationError, AccessError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def remove_spaces(self):
        for product in self.env['product.template'].search([('name', 'like', ' %')]):
            # print('product.name.lstrip()',product.name.lstrip())
            product.write({'name': product.name.lstrip()})
