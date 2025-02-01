from odoo import models, fields, api

class InheritHrContract(models.Model):
    _inherit = "hr.contract"

    medical_insurance_id = fields.Many2one('medical.insurance')
    layer_id = fields.Many2one('medical.insurance.layers')
    layers_ids = fields.One2many(related='medical_insurance_id.layers_ids')
    medical_amount = fields.Monetary(related='layer_id.amount')
