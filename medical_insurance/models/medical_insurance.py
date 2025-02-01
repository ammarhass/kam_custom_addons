from odoo import models, fields, api

class MedicalInsurance(models.Model):
    _name = "medical.insurance"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _description = "Medical Insurance"

    name = fields.Char()
    contact_person_id = fields.Many2one('res.partner')
    customer_id = fields.Many2one('res.partner')
    start_date = fields.Date()
    end_date = fields.Date()
    layers_ids = fields.One2many('medical.insurance.layers', 'medical_insurance_id')

