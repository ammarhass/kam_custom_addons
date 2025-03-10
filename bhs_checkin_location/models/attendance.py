from odoo import models, fields, tools, api
from datetime import datetime
import pytz
class BHHrAttendance(models.Model):
    _inherit = 'hr.attendance'

    attendance_location = fields.Many2one('hr.attendance.location.vision', 'Check in location', default=lambda self: self.env.ref('bhs_checkin_location.attendance_location_company', raise_if_not_found=False))
    gate = fields.Char()

    @api.model
    def create(self, values):
        if self.env.context.get('current_location'):
            values['attendance_location'] = self.env.context.get('current_location')

        return super(BHHrAttendance, self).create(values)



