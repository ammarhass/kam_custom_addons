# models/res_users.py
from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    pos_config_ids = fields.Many2many(
        'pos.config',
        string="Assigned POS Configurations",
        help="POS Configurations assigned to the user."
    )
