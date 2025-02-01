from odoo import models, fields, api, _


class InheritAccountJournal(models.Model):
    _name = 'audit.note'

    name = fields.Char()