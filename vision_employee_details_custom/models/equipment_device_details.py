from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class EquipmentDevice(models.Model):
    _name = 'equipment.device.details'

    name = fields.Char()
    date = fields.Date()
    date_to = fields.Date()
    employee_id = fields.Many2one('hr.employee')


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    equipment_device_ids = fields.One2many('equipment.device.details', 'employee_id')
