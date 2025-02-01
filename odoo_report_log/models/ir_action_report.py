# -*- coding: utf-8 -*-

import base64

from odoo import models, fields


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    create_log = fields.Boolean("Create log when report is printed", default=True)
    log_attachment = fields.Boolean()

    def _render_qweb_pdf(self, report_ref, res_ids=None, data=None):
        log = self.env['report.log']
        # Create & commit log record
        report_log = self._get_report(report_ref)
        if report_log.create_log:
            log_values = {
                'report_id': report_log.id,
                'res_model': report_log.model,
                'user_id': self.env.user.id,
                'date': fields.Datetime.now(),
                'state': 'fail',  # default is failed, updated when report is generated
            }
            if res_ids:
                log_values['res_ids'] = f'[{res_ids}]' if isinstance(res_ids, int) else str(res_ids)
            log = self.env['report.log'].sudo().create(log_values)
            self.env.cr.commit()

        try:
            pdf_content, type = super(IrActionsReport, self)._render_qweb_pdf(report_ref, res_ids=res_ids, data=data)

            if report_log.create_log:
                log_update_values = {
                    'state': 'success'
                }
                # Add report content if log_attachment is set
                if report_log.log_attachment:
                    log_update_values.update({'report_content': base64.b64encode(pdf_content), 'report_file_name': f'{self.name}.pdf'})
                log.write(log_update_values)
        except Exception as e:
            if log:
                log.write({'fail_message': e})
                self.env.cr.commit()
            raise e

        return pdf_content, type

    def action_view_report_logs(self):
        return {
            'type': 'ir.actions.act_window',
            'name': "Logs",
            'res_model': 'report.log',
            'view_type': 'list',
            'view_mode': 'list',
            'views': [[False, 'list']],
            'domain': [('report_id', '=', self.id)],
        }
