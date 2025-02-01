from odoo import models, fields, api
from odoo.exceptions import ValidationError


class InheritAccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    @api.model
    def create(self, vals):
        if 'price_unit' in vals:
            product = self.env['product.product'].browse(vals.get('product_id'))
            if product.lst_price > vals['price_unit']:
                raise ValidationError(f"Price can't be lower than {product.lst_price}")
        return super().create(vals)

    def write(self, vals):
        if 'price_unit' in vals:
            if not self.user_has_groups('elhegaz_sales_custom.manager_access_product_price_invoice'):
                if vals.get('price_unit') < self.price_unit:
                    raise ValidationError(f"Price can't be lower than {self.price_unit}")
        return super().write(vals)

