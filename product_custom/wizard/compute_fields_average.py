from odoo import models, fields, api
from datetime import datetime, date, timedelta
import math


def compute_total_quantity(sellers):
    sellers_mapped = sellers.mapped('min_qty')
    precision = 3
    floored_values = [round(val - 0.001, precision) if val * 100 ** precision % 1 else val for val in sellers_mapped]
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
    _name = 'fields.average'

    total_quantity = fields.Float(readonly=True, digits=(12, 4))
    total_white_rice = fields.Float(readonly=True, digits=(12, 4))
    total_fraction = fields.Float(readonly=True, digits=(12, 4))
    total_good_rice = fields.Float(readonly=True, digits=(12, 4))
    total_soft_fraction = fields.Float(readonly=True, digits=(12, 4))
    total_hard_fraction = fields.Float(readonly=True, digits=(12, 4))
    hadr = fields.Float(readonly=True, digits=(12, 4))
    rageaa = fields.Float(readonly=True, digits=(12, 4))
    sersa = fields.Float(readonly=True, digits=(12, 4))
    white_rice_average = fields.Float(readonly=True, digits=(12, 4))
    fraction_average = fields.Float(readonly=True, digits=(12, 4))
    good_rice_average = fields.Float(readonly=True, digits=(12, 4))
    barley_rice_average = fields.Float(readonly=True, digits=(12, 4))
    date_from = fields.Date()
    date_to = fields.Date()
    partner_ids = fields.Many2many('res.partner')

    @api.onchange('date_from', 'date_to')
    def date_onchange_fun(self):
        if self.date_from and self.date_to:
            self.compute_all_fields_average()

    @api.onchange('partner_ids')
    def partner_onchange_fun(self):
        self.compute_all_fields_average()

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
                self.total_soft_fraction = self.total_quantity * 0.02
                self.total_hard_fraction = self.total_fraction - self.total_soft_fraction
                self.rageaa = self.total_quantity * 0.1
                self.hadr = self.total_quantity * 0.03
                self.sersa = self.total_quantity - (self.total_good_rice + self.total_fraction + self.rageaa + self.hadr)
                self.white_rice_average = self.total_white_rice / self.total_quantity
                self.fraction_average = self.total_fraction / self.total_white_rice
                self.good_rice_average = self.total_good_rice / self.total_quantity
                self.barley_rice_average = self.total_quantity / self.total_good_rice
            else:
                self.total_quantity, self.total_white_rice, self.total_fraction, self.total_good_rice, self.white_rice_average, self.fraction_average, \
                self.good_rice_average, self.barley_rice_average, self.total_soft_fraction, self.total_hard_fraction, self.hadr, self.rageaa, self.sersa  = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

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
