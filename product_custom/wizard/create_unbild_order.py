from odoo import models, fields, api
from datetime import datetime, date, timedelta
import math
from decimal import *


from odoo.tools.populate import compute


def compute_total_quantity(sellers):
    sellers_mapped = sellers.mapped('min_qty')
    precision = 2
    floored_values = [round(val - 0.01, precision) if val * 10 ** precision % 1 else val for val in sellers_mapped]
    return sum(floored_values)


def compute_total_white_rice_quantity(sellers):
    sellers_mapped = sellers.mapped('white_rice_quantity')
    precision = 3
    floored_values = [round(val - 0.001, precision) if val * 100 ** precision % 1 else val for val in sellers_mapped]
    return sum(floored_values)

def compute_total_fraction(sellers):
    sellers_mapped = sellers.mapped('fraction_quantity')
    precision = 3
    floored_values = [round(val - 0.001, precision) if val * 100 ** precision % 1 else val for val in sellers_mapped]
    return sum(floored_values)


def compute_total_good_rice(sellers):
    sellers_mapped = sellers.mapped('good_rice_quantity')
    precision = 3
    floored_values = [round(val - 0.001, precision) if val * 100 ** precision % 1 else val for val in sellers_mapped]
    return sum(floored_values)



class FieldsAverage(models.TransientModel):
    _name = 'create.unbuild.order'

    white_rice = fields.Float(digits=(12, 3))
    actual_fraction_value = fields.Float(digits=(12, 3))
    actual_quantity = fields.Float(compute='_compute_actual_total_quantity', digits=(12, 3))

    total_quantity = fields.Float(readonly=True, digits=(12, 3))
    total_white_rice = fields.Float(readonly=True, digits=(12, 3))
    total_fraction = fields.Float(readonly=True, digits=(12, 3))
    total_good_rice = fields.Float(readonly=True, digits=(12, 3))
    total_soft_fraction = fields.Float(readonly=True, digits=(12, 3))
    total_hard_fraction = fields.Float(readonly=True, digits=(12, 3))
    hadr = fields.Float(readonly=True, digits=(12, 3))
    rageaa = fields.Float(readonly=True, digits=(12, 3))
    sersa = fields.Float(readonly=True, digits=(12, 3))
    white_rice_average = fields.Float(readonly=True)
    fraction_average = fields.Float(readonly=True)
    good_rice_average = fields.Float(readonly=True)
    barley_rice_average = fields.Float(readonly=True)
    date_from = fields.Date()
    date_to = fields.Date()
    partner_ids = fields.Many2many('res.partner')

    # @api.onchange('date_from', 'date_to')
    # def date_onchange_fun(self):
    #     if self.date_from and self.date_to:
    #         self.compute_all_fields_average()
    #
    # @api.onchange('partner_ids')
    # def partner_onchange_fun(self):
    #     self.compute_all_fields_average()

    @api.depends('white_rice', 'actual_fraction_value')
    def _compute_actual_total_quantity(self):
        self.compute_all_fields_average()
        self.actual_quantity = (self.white_rice - (self.white_rice * self.actual_fraction_value)) * self.barley_rice_average

    def test(self):
        quantities = []
        quantities.append(self.white_rice)
        active_id = self.env.context.get('active_id')
        rec = self.env['product.template'].search([('id', '=', active_id)])
        bom_id = self.env['mrp.bom'].search([('product_tmpl_id.id', '=', active_id)], limit=1)
        total_white_rice = self.actual_quantity * self.white_rice_average
        soft_fraction = self.actual_quantity * 0.02
        fraction_quantity = ((total_white_rice * self.fraction_average) - (self.white_rice * self.actual_fraction_value)) - soft_fraction
        quantities.append(fraction_quantity)
        quantities.append(soft_fraction)
        rageea = self.actual_quantity * 0.1
        quantities.append(rageea)
        hadr = self.actual_quantity * 0.03
        quantities.append(hadr)
        sersa = self.actual_quantity - (self.white_rice + fraction_quantity + hadr + rageea + soft_fraction)
        quantities.append(sersa)
        i = 0
        for line in bom_id.bom_line_ids:
            bom_id.write({
                'bom_line_ids': [(1, line.id, {
                    'product_qty': quantities[i] / self.actual_quantity,
                })]
            })
            i += 1

        vals = {
            'product_id': bom_id.product_id.id,
            'bom_id': bom_id.id,
            'product_qty': self.actual_quantity
        }
        a = self.env['mrp.unbuild'].sudo().with_context(default_unbuild_order_percentage = True).create(vals)
        a._onchange_bom_id()
        print(a.state)

    def compute_all_fields_average(self):
        active_id = self.env.context.get('active_id')
        rec = self.env['product.template'].search([('id', '=', active_id)])
        if not self.date_from or not self.date_to:
            if self.partner_ids:
                filtered_sellers = rec.seller_ids.filtered(lambda x: x.partner_id.id in self.partner_ids.ids)
            else:
                filtered_sellers = rec.seller_ids
            if filtered_sellers:
                self.total_quantity = compute_total_quantity(filtered_sellers)
                self.total_white_rice = compute_total_white_rice_quantity(filtered_sellers)
                self.total_fraction = compute_total_fraction(filtered_sellers)
                self.total_good_rice = compute_total_good_rice(filtered_sellers)
                self.total_soft_fraction = self.total_fraction * 0.2
                self.total_hard_fraction = self.total_fraction - self.total_soft_fraction
                self.rageaa = self.total_quantity * 0.1
                self.hadr = self.total_quantity * 0.03
                self.sersa = self.total_quantity - (
                            self.total_white_rice + self.total_fraction + self.rageaa + self.hadr)
                self.white_rice_average = self.total_white_rice / self.total_quantity
                self.fraction_average = self.total_fraction / self.total_white_rice
                self.good_rice_average = self.total_good_rice / self.total_quantity
                self.barley_rice_average = self.total_quantity / self.total_good_rice
            else:
                self.total_quantity, self.total_white_rice, self.total_fraction, self.total_good_rice, self.white_rice_average, self.fraction_average, \
                    self.good_rice_average, self.barley_rice_average, self.total_soft_fraction, self.total_hard_fraction, self.hadr, self.rageaa, self.sersa = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

        elif self.date_from and self.date_to:
            if self.partner_ids:
                filtered_sellers = rec.seller_ids.filtered(
                    lambda x: x.date and isinstance(x.date,
                                                    date) and self.date_from <= x.date <= self.date_to).filtered(
                    lambda x: x.partner_id.id in self.partner_ids.ids)
            else:
                filtered_sellers = rec.seller_ids.filtered(
                    lambda x: x.date and isinstance(x.date, date) and self.date_from <= x.date <= self.date_to)
            if filtered_sellers:
                self.total_quantity = compute_total_quantity(filtered_sellers)
                self.total_white_rice = compute_total_white_rice_quantity(filtered_sellers)
                self.total_fraction = compute_total_fraction(filtered_sellers)
                self.total_good_rice = compute_total_good_rice(filtered_sellers)
                self.white_rice_average = self.total_white_rice / self.total_quantity
                self.fraction_average = self.total_fraction / self.total_white_rice
                self.good_rice_average = self.total_good_rice / self.total_quantity
                self.barley_rice_average = self.total_quantity / self.total_good_rice
            else:
                self.total_quantity, self.total_white_rice, self.total_fraction, self.total_good_rice, self.white_rice_average, self.fraction_average, self.good_rice_average, self.barley_rice_average = 0, 0, 0, 0, 0, 0, 0, 0

        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'fields.average',
            'res_id': self.id,
            'view_id': self.env.ref('product_custom.fields_average_wizard_form').id,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

    # filtered(lambda x: self.date_from <= x.date <= self.date_to)

    # def compute_all_fields_average(self):
    #     active_id = self.env.context.get('active_id')
    #     rec = self.env['product.template'].search([('id', '=', active_id)])
    #     if not self.date_from or not self.date_to:
    #         self.total_quantity = sum(rec.seller_ids.mapped('min_qty'))
    #         self.total_white_rice = sum(rec.seller_ids.mapped('white_rice_quantity'))
    #         self.total_fraction = sum(rec.seller_ids.mapped('fraction_quantity'))
    #         self.total_good_rice = sum(rec.seller_ids.mapped('good_rice_quantity'))
    #         self.white_rice_average = self.total_white_rice / self.total_quantity
    #         self.fraction_average = self.total_fraction / self.total_white_rice
    #         self.good_rice_average = self.total_good_rice / self.total_quantity
    #     elif self.date_from and self.date_to:
    #         filtered_sellers = rec.seller_ids.filtered(
    #             lambda x: x.date and isinstance(x.date, date) and self.date_from <= x.date <= self.date_to)
    #         self.total_quantity = sum(filtered_sellers.mapped('min_qty'))
    #         self.total_white_rice = sum(filtered_sellers.mapped('white_rice_quantity'))
    #         self.total_fraction = sum(filtered_sellers.mapped('fraction_quantity'))
    #         self.total_good_rice = sum(filtered_sellers.mapped('good_rice_quantity'))
    #         self.white_rice_average = self.total_white_rice / self.total_quantity
    #         self.fraction_average = self.total_fraction / self.total_white_rice
    #         self.good_rice_average = self.total_good_rice / self.total_quantity
