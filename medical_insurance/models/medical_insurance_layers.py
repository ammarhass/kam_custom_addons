from odoo import models, fields, api

class MedicalInsuranceLayers(models.Model):
    _name = 'medical.insurance.layers'

    name = fields.Char()
    amount = fields.Monetary()
    currency_id = fields.Many2one(
        'res.currency', string='Currency', required=True,
        default=lambda self: self.env.user.company_id.currency_id.id)

    medical_insurance_id = fields.Many2one('medical.insurance')
