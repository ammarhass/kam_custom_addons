from odoo import models, fields, api


class OperationGeneral(models.Model):
    _name = 'operation.general'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'confirmed'),
        ('submit', 'submitted To Cost'),
        ('cost_confirm', 'Cost Confirmed'),
        ('account_submit', 'Account Submitted'),
        ('account_confirm', 'Account Confirmed'),
        ('final_confirm', 'Final Confirm')
    ], default='draft')

    user_three_access = fields.Boolean(compute='_compute_is_allowed_user_three')
    user_four_access = fields.Boolean(compute='_compute_is_allowed_user_four')

    def _compute_is_allowed_user_three(self):
        for record in self:
            user = self.env.user
            allowed_group = self.env.ref('operation.operation_access_user_three')
            record.user_three_access = user in allowed_group.users

    def _compute_is_allowed_user_four(self):
        for record in self:
            user = self.env.user
            allowed_group = self.env.ref('operation.operation_access_user_four')
            record.user_four_access = user in allowed_group.users

    name = fields.Char()

    supplier_id = fields.Many2one('res.partner')
    customer_id = fields.Many2one('res.partner')
    customer_name = fields.Char()
    po_number = fields.Char()
    truck_type_id = fields.Many2one('truck.type')
    truck_type = fields.Char()
    driver = fields.Char()
    phone = fields.Integer()
    truck_license = fields.Char()
    from_from = fields.Char()
    to_to = fields.Char()
    req_date = fields.Date()

    loading_date = fields.Date()
    loading_arrival_time = fields.Datetime()
    approval_time = fields.Datetime()
    departure_date = fields.Date()
    departure_time = fields.Datetime()
    over_time = fields.Integer()
    over_night = fields.Integer()

    delivery_date = fields.Date()
    arrival_time = fields.Datetime()
    destination_departure_date = fields.Date()
    destination_departure_time = fields.Datetime()
    destination_over_time = fields.Integer()
    destination_over_night = fields.Integer()

    delegates = fields.Char()
    labor = fields.Char()
    drop = fields.Char()
    return_return = fields.Char()
    notes = fields.Text()
    additional_notes = fields.Text()
    extra_notes = fields.Text()

    nolon = fields.Float()
    custody = fields.Float()
    payment_number = fields.Char()
    final_nolon = fields.Float(compute='compute_final_nolon')
    drop_overnight = fields.Float()
    labour = fields.Float()
    elastic = fields.Float()
    tolls_and_scales = fields.Float()
    commission = fields.Float()
    total_transportation = fields.Float(compute='compute_total_transportation')

    client_overnight = fields.Float()
    client_drop = fields.Float()
    client_return = fields.Float()
    client_delegate = fields.Float()
    client_labour = fields.Float()
    client_nolon = fields.Float()
    client_total = fields.Float(compute='compute_client_total')
    road_crossing = fields.Float()
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company.id)

    total_account_id = fields.Many2one('account.account')
    road_crossing_account_id = fields.Many2one('account.account')
    total_transportation_account_id = fields.Many2one('account.account')

    group_two = fields.Boolean(compute='compute_group_two_users')
    group_three = fields.Boolean(compute='compute_group_three_users')
    group_four = fields.Boolean(compute='compute_group_four_users')

    @api.depends('client_overnight', 'client_drop', 'client_return', 'client_delegate', 'client_labour', 'client_nolon')
    def compute_client_total(self):
        for rec in self:
            rec.client_total = rec.client_overnight + rec.client_drop + rec.client_return + rec.client_delegate + rec.client_labour + rec.client_nolon

    @api.depends('final_nolon', 'drop_overnight', 'labour', 'elastic', 'tolls_and_scales', 'commission',
                 'total_transportation')
    def compute_total_transportation(self):
        for rec in self:
            rec.total_transportation = rec.final_nolon + rec.drop_overnight + rec.labour + rec.elastic + rec.tolls_and_scales + rec.commission

    @api.depends('nolon', 'custody')
    def compute_final_nolon(self):
        for rec in self:
            rec.final_nolon = rec.nolon - rec.custody

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_submit_to_cost(self):
        for rec in self:
            rec.state = 'submit'

    def action_cost_confirmed(self):
        for rec in self:
            rec.state = 'cost_confirm'

    def action_submit_to_account(self):
        for rec in self:
            rec.state = 'account_submit'

    def action_account_confirm(self):
        for rec in self:
            rec.state = 'account_confirm'

    def create_invoice_bill(self):
        invoice_data = [{
            'move_type': 'out_invoice',  # 'out_invoice' for customer invoices
            'partner_id': self.customer_id.id,  # Replace with actual customer ID
            'date': fields.Date.today(),
        },
            {
                'move_type': 'in_invoice',  # 'out_invoice' for customer invoices
                'partner_id': self.supplier_id.id,  # Replace with actual customer ID
                'date': fields.Date.today(),
            }]

        invoices = self.env['account.move'].create(invoice_data)
        for invoice in invoices:
            if invoice.move_type == 'out_invoice':
                invoice.write({'line_ids': [
                    (0, 0, {'account_id': self.total_account_id.id, 'display_type': 'product', 'name': 'Total'}),
                    (0, 0, {'account_id': self.road_crossing_account_id.id, 'display_type': 'product',
                            'name': 'Road Crossing'})]})
                invoice.sudo().invoice_line_ids[0].price_unit = self.client_total
                invoice.sudo().invoice_line_ids[1].price_unit = self.road_crossing
            elif invoice.move_type == 'in_invoice':
                invoice.sudo().write({'line_ids': [
                    (0, 0, {'account_id': self.total_transportation_account_id.id, 'display_type': 'product',
                            'name': 'Total Transportation'}), ]})
                invoice.sudo().invoice_line_ids[0].price_unit = self.total_transportation
        self.state = 'final_confirm'

# 'invoice_line_ids': [
#                     (0, 0, {
#                         # 'product_id': self.env.ref('product.product_product_1').id,  # Replace with actual product ID
#                         # 'quantity': 1,
#                         'price_unit': self.client_total,
#                         # 'name': 'Total',
#                         # 'account_id': self.total_account_id.id
#                     }),
#                     (0, 0, {
#                         # 'product_id': self.env.ref('product.product_product_2').id,  # Replace with actual product ID
#                         # 'quantity': 1,
#                         'price_unit': self.road_crossing,
#                         # 'name': 'Road Crossing',
#                         # 'account_id': self.road_crossing_account_id.id
#                     }),
#                 ],
#                 'line_ids': [
#                     (0, 0, {
#                         # 'product_id': self.env.ref('product.product_product_1').id,  # Replace with actual product ID
#                         'account_id': self.total_account_id.id,
#                         'display_type': 'product',
#                         'name': "Total"
#                     }),
#                     (0, 0, {
#                         # 'product_id': self.env.ref('product.product_product_1').id,  # Replace with actual product ID
#                         'account_id': self.road_crossing_account_id.id,
#                         'display_type': 'product',
#                         'name': "Road Crossing"
#                     }),
#                 ],
