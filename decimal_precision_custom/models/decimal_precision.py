from odoo import models, fields, api, tools


class DecimalPrecision(models.Model):
    _inherit = 'decimal.precision'
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.company)

    _sql_constraints = [

    ]

    @api.model
    @tools.ormcache('application', 'self.env.company.id')
    def precision_get(self, application):
        # Get the current company
        company_id = self.env.company.id

        self.flush_model(['name', 'digits', 'company_id'])
        self.env.cr.execute('''
            SELECT digits 
            FROM decimal_precision 
            WHERE name=%s AND (company_id=%s OR company_id IS NULL)
            ORDER BY company_id DESC
            LIMIT 1
        ''', (application, company_id))

        res = self.env.cr.fetchone()
        return res[0] if res else 2
