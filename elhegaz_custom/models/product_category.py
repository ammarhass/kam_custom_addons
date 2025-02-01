from odoo import models, fields, api


class InheritProductCategory(models.Model):
    _inherit = 'product.category'

    branch_id = fields.Many2one('res.branch')
    test = fields.Char()