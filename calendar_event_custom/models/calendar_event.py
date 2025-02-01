from odoo import models, fields, api, _

class CalendaryEvent(models.Model):
    _inherit = 'calendar.event'

    address = fields.Char()