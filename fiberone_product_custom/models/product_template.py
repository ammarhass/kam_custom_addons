from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    additional_cost_currency_id = fields.Many2one('res.currency', string='Additional Cost Currency', default=lambda self: self.env.ref('base.EUR'))
    additional_cost = fields.Monetary('Additional Cost', currency_field='additional_cost_currency_id', compute='_onchange_standard_price')
    total_additional_cost = fields.Monetary(string="Total Value", compute='_compute_standard_price', compute_sudo=True, currency_field='additional_cost_currency_id')
    default_sequence = fields.Char()
    eg_code = fields.Char()
    number_part = fields.Char()
    manufactured_company = fields.Char()

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if val.get('categ_id'):
                self._update_reference_number(val)
        return super().create(vals_list)

    def write(self, vals):
        if 'categ_id' in vals:
            self._update_reference_number(vals)
        return super().write(vals)

    def _update_reference_number(self, vals):
        category = self.env['product.category'].browse(vals['categ_id'])
        if category.prefix:
            prefix = category.prefix.replace(' ', '_') + '_'
        else:
            prefix = ''

        all_words = prefix + str(len((self.env['product.template'].search([('categ_id', '=', vals['categ_id'])]))) + 1)
        string_without_spaces = all_words.replace(" ", "")
        vals['default_sequence'] = string_without_spaces
        self.env['product.category'].browse(vals['categ_id']).write({'sequence': string_without_spaces})
        return True

    @api.depends('standard_price', 'additional_cost_currency_id', 'additional_cost')
    def _onchange_standard_price(self):
        for rec in self:
            if rec.additional_cost_currency_id:
                company_currency = self.env.company.currency_id
                rec.additional_cost = company_currency._convert(
                    rec.standard_price if rec.qty_available else 0,
                    rec.additional_cost_currency_id,
                    self.env.company,
                    fields.Date.today()
                )
                rec.total_additional_cost = rec.additional_cost * rec.sudo(False).qty_available
