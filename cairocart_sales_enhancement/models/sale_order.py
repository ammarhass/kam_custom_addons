from odoo import models, fields, api, tools, _
from odoo.exceptions import MissingError, ValidationError, AccessError

class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    driver_num = fields.Char(string="Driver Number", required=False, )

    @api.model
    def create(self, vals):
        if 'name' in vals:
            existing_order = self.search([('name', '=', vals['name'])], limit=1)
            if existing_order:
                raise ValidationError(
                    f"The sale order name '{vals['name']}' already exists. Please provide a unique name.")
        return super(SaleOrderInherit, self).create(vals)