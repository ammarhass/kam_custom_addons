from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.company'

    is_gadara = fields.Boolean(string="Is Gadara",  )