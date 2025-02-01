from odoo import models, fields, api


class TruckType(models.Model):
    _name = 'truck.type'

    name = fields.Char()
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company.id)