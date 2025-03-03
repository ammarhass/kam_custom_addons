from odoo import  models, api, fields


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'


    def open_wizard(self):
        action = {
            'type': 'ir.actions.act_window',
            'res_model': 'auto_carrier',
            'target': 'new',
            'views': [(self.env.ref('inventory_enhancement.auto_carrier_form').id, 'form')],
        }

        # print('action2', action)
        return action

    def _auto_fill_carrier(self, carrier):
        context = dict(self._context or {})
        active_ids = context.get('active_ids')
        records = self.browse(active_ids)
        for record in records:

            record.carrier_id = carrier