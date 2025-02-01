from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends('order_line.price_total')
    def _amount_all(self):
        """ Compute the total amounts of the SO. """
        for order in self:
            amount_untaxed = amount_tax = amount_discount = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
                amount_discount += (line.product_uom_qty *
                                    line.price_unit * line.discount)/100
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_discount': amount_discount,
                'amount_total': amount_untaxed + amount_tax,
            })

    discount_type = fields.Selection(
        [('percent', 'Percentage'), ('amount', 'Amount')],
        string='Discount type',
        readonly=True,
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        default='percent')
    discount_rate = fields.Float('Discount Rate',
                                 digits=dp.get_precision('Discount'),
                                 readonly=True,
                                 states={'draft': [('readonly', False)],
                                         'sent': [('readonly', False)]})
    amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True,
                                     readonly=True, compute='_amount_all',
                                     track_visibility='always')
    amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True,
                                 compute='_amount_all',
                                 track_visibility='always')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True,
                                   compute='_amount_all',
                                   track_visibility='always')
    amount_discount = fields.Monetary(string='Discount', store=True,
                                      readonly=True, compute='_amount_all',
                                      digits=dp.get_precision('Discount'),
                                      track_visibility='always')

    @api.onchange('discount_type', 'discount_rate', 'order_line')
    def supply_rate(self):
        """supply discount into order line"""
        for order in self:
            if order.discount_type == 'percent' and order.discount_rate > 0:
                for line in order.order_line:
                    line.discount = order.discount_rate
            elif order.discount_rate > 0:
                total = discount = 0.0
                for line in order.order_line:
                    total += (line.product_uom_qty * line.price_unit)
                if order.discount_rate != 0:
                    discount = (order.discount_rate / total) * 100
                else:
                    discount = order.discount_rate
                for line in order.order_line:
                    line.discount = discount
                    new_sub_price = (line.price_unit * (discount / 100))
                    line.total_discount = line.price_unit - new_sub_price

    def _prepare_invoice(self, ):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals.update({
            'discount_type': self.discount_type,
            'discount_rate': self.discount_rate,
            'amount_discount': self.amount_discount,
        })
        return invoice_vals

    def button_dummy(self):

        self.supply_rate()
        return True



class SaleOrderLine(models.Model):
    """Inherit sale order  line and add fields"""
    _inherit = "sale.order.line"
    total_discount = fields.Float(string="Total Discount", default=0.0,
                                  store=True)
