from odoo import models, fields, api


class NewReportPaymentCheck(models.AbstractModel):
    _name = 'report.vision_employee_details_custom.employee_details_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        employee = self.env['hr.employee'].browse(docids)
        promotion_details = employee.promotion_details_ids
        equipment_device_details = employee.equipment_device_ids

        query = self.env['employee.info']._search(
            [('employee_id', '=', employee.id)])
        query.order = None
        query_string, query_param = query.select('DISTINCT employee_info.training_id')
        self._cr.execute(query_string, query_param)
        training_id_all = [line.get('training_id') for line in self._cr.dictfetchall()]
        training_ids = self.env['employee.training'].browse(training_id_all)


        docs = {
            'docs': employee,
            'Promotions': promotion_details,
            'Equipments': equipment_device_details,
            'Trainings': training_ids
        }
        return docs




