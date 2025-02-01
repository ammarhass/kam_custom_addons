from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'
    #
    # additional_cost_currency_id = fields.Many2one('res.currency', string='Additional Cost Currency', default=lambda self: self.env.ref('base.EUR'))
    # additional_cost = fields.Monetary('Additional Cost', currency_field='additional_cost_currency_id', compute='_onchange_standard_price')
    # total_additional_cost = fields.Monetary(string="Total Value", compute='_compute_standard_price', compute_sudo=True, currency_field='additional_cost_currency_id')

    @api.model
    def create(self, vals_list):
        res = super().create(vals_list)
        print("i")
        return res


    @api.depends('standard_price', 'additional_cost_currency_id', 'additional_cost')
    def _onchange_standard_price(self):
        for rec in self:
            if rec.additional_cost_currency_id:
                company_currency = self.env.company.currency_id
                rec.additional_cost = company_currency._convert(
                    rec.standard_price,
                    rec.additional_cost_currency_id,
                    self.env.company,
                    fields.Date.today()
                )
                rec.total_additional_cost = rec.additional_cost * rec.sudo(False).qty_available