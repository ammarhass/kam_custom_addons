from odoo import models, fields, api


class PosWizard(models.TransientModel):
    _name = 'pos.category.wizard'

    limit = fields.Float()

    def apply_action(self):
        active_id = self.env.context.get('active_id')
        categories = self.env['pos.category'].search([])
        if categories:
            for cat in categories:
                cat.discount_limit = self.limit
        return {'type': 'ir.actions.act_window_close'}
