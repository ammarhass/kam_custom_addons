from odoo import models, fields


class CheckInOut(models.TransientModel):
    _name = 'auto_carrier'
    _description = 'auto_carrier'

    carrier_id = fields.Many2one('delivery.carrier', 'Carrier', required=True, ondelete='cascade')

    def apply_auto_fill_carrier(self):
        carrier = self.carrier_id
        # date_to = self.date2

        # Call the method to auto-checkout employees within the specified date range
        self.env['stock.picking']._auto_fill_carrier(carrier)

    # def confirm(self):
    #     pass
    # # attendance_id = fields.Many2one(comodel_name="hr.attendance", string="attendance", required=False, )
