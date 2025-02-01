from odoo import models, fields, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    product_cost = fields.Float(related='product_id.standard_price', store=True)