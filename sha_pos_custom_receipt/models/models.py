from odoo import api, fields, models, _


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    emp_name = fields.Char("Receipt Name")


class PosSessionInherit(models.Model):
    _inherit = 'pos.session'

    def _loader_params_hr_employee(self):
        params = super()._loader_params_hr_employee()
        # this is usefull to evaluate reward domain in frontend
        params['search_params']['fields'].append('emp_name')
        return params
