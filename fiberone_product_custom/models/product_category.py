from odoo import models, fields, api


class InheritProductCategory(models.Model):
    _inherit = 'product.category'

    prefix = fields.Char()
    sequence = fields.Char()

    def update_product_sequence(self):

        categories = self.env['product.category'].search([])
        for cat in categories:
            sequence_number = 1
            sequence = ''
            products = self.env['product.product'].search(domain=[('categ_id', '=', cat.id)], order='id')
            for product in products:
                if cat.prefix:
                    prefix = cat.prefix.replace(' ', '_') + '_'
                else:
                    prefix = ''
                all_words = prefix + str(sequence_number)
                default_code = all_words.replace(" ", "")
                product.write(
                    {
                        "default_code": default_code,
                    }
                )
                sequence_number = sequence_number + 1
                sequence = default_code
            cat.sequence = sequence