# -*- coding: utf-8 -*-

from odoo import models, fields, _

import json


class ReportLog(models.Model):
    _name = 'report.log'
    _description = 'Report Log'
    _rec_name = 'id'
    _order = 'id desc'

    report_id = fields.Many2one('ir.actions.report', string="Report")
    date = fields.Datetime()
    user_id = fields.Many2one('res.users', string="User")
    res_model = fields.Char(string='Model')
    res_ids = fields.Char(string="Resources")
    report_content = fields.Binary(string="Report Attachment")
    report_file_name = fields.Char()
    state = fields.Selection([('fail', 'Failed'), ('success', 'Successful')], string="Status")
    fail_message = fields.Text(string="Error Message")
    company_id = fields.Many2one('res.company', 'Company', index=True, default=lambda self: self.env.company)

    def action_view_record(self):
        res_ids = json.loads(self.res_ids)
        if len(res_ids) == 1:
            return {
                'type': 'ir.actions.act_window',
                'res_model': self.res_model,
                'view_type': 'form',
                'view_mode': 'form',
                'views': [[False, 'form']],
                'res_id': res_ids[0]
            }
        return {
            'type': 'ir.actions.act_window',
            'name': self.env[self.res_model]._description,
            'res_model': self.res_model,
            'view_type': 'list',
            'view_mode': 'list',
            'views': [[False, 'list'], [False, 'form']],
            'domain': [('id', 'in', res_ids)],
        }

