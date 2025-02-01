from odoo import models, fields, api


class CRMLeadInherit(models.Model):
    _inherit = 'crm.lead'

    @api.depends('team_id', 'type')
    def _compute_stage_id(self):
        for lead in self:
            if not lead.stage_id:
                lead.stage_id = lead._stage_find(domain=[('fold', '=', False), ('company_id', 'in', self.env.companies.ids)]).id
