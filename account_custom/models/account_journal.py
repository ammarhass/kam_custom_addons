from odoo import models, fields, api, _
from odoo.exceptions import UserError


class InheritAccountJournal(models.Model):
    _inherit = 'account.journal'

    def write(self, vals):
        if 'restrict_mode_hash_table' in vals:
            restrict_mode_hash_table = vals.pop('restrict_mode_hash_table')
            self.env.cr.execute("""
                UPDATE account_journal
                SET restrict_mode_hash_table = %s
                WHERE id IN %s
            """, (restrict_mode_hash_table, tuple(self.ids)))

        try:
            return super().write(vals)
        except exceptions.UserError as e:
            raise e
