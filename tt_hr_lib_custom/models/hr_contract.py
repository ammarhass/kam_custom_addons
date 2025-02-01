from odoo import models, fields, api
from odoo.addons.test_impex.models import field


class HrContract(models.Model):
    _inherit = 'hr.contract'

    company_insurance = fields.Float("Company Insurance")