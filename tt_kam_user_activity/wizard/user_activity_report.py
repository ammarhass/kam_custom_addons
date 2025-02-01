from odoo import models, fields, api
from datetime import datetime, time

class UserActivityReport(models.TransientModel):
    _name = 'user.activity.report'
    _rec_name = 'user_id'
    _description = 'User Activity Report'

    date_from = fields.Date(string="Date From", required=False)
    date_to = fields.Date(string="Date To", required=False)
    user_id = fields.Many2one(comodel_name="res.users", string="User Name", required=False)
    company_ids = fields.Many2many(comodel_name="res.company", string="Companies",
                                   domain=lambda self: [('id', 'in', self.env.user.company_ids.ids)])

    def print_user_activity_report(self):
        # Retrieve the report action from the ir.actions.report model
        report_action = self.env['ir.actions.report'].search([
            ('report_name', '=', 'tt_kam_user_activity.user_activity_template')
        ], limit=1)

        # if not report_action:
        #     raise UserError("The report action 'tt_kam_user_activity.user_activity_template' was not found.")

        return report_action.report_action(self)


class ParticularReport(models.AbstractModel):
    _name = 'report.tt_kam_user_activity.user_activity_template'

    @api.model
    def _get_report_values(self, docids, data=None):
        report_obj = self.env['ir.actions.report']  # create an object from report model
        report = report_obj._get_report_from_name(
            'tt_kam_user_activity.user_activity_template')  # create an object from report action

        model_id = self.env[report.model].browse(docids)
        journal_entries = self.create_domain('account.move', model_id, 'entry')
        customer_invoices = self.create_domain('account.move', model_id, 'in_invoice')
        vendor_bills = self.create_domain('account.move', model_id, 'out_invoice')
        # sale_receipts = self.create_domain('account.voucher', model_id, 'in_invoice')
        # purchase_receipts = self.create_domain('account.voucher', model_id, 'out_invoice')
        payments = self.create_domain('account.payment', model_id)
        COA = self.create_domain('account.account', model_id)
        partners = self.create_domain('res.partner', model_id)
        products = self.create_domain('product.template', model_id)
        categories = self.create_domain('product.category', model_id)
        mrp = self.create_domain('mrp.production', model_id)
        stock_picking = self.create_domain('stock.picking', model_id)
        # stock_inventory = self.create_domain('stock.inventory', model_id)
        stock_warehouse = self.create_domain('stock.warehouse', model_id)

        vals = {
            'doc_ids': docids,  # Record Id
            'doc_model': report.model,  # Model Name
            'docs': self.env[report.model].browse(docids),  # Record Of Model
            'journal_entries': journal_entries,
            'customer_invoices': customer_invoices,
            'vendor_bills': vendor_bills,
            # 'sale_receipts': sale_receipts,
            # 'purchase_receipts': purchase_receipts,
            'payments': payments,
            'COA': COA,
            'partners': partners,
            'products': products,
            'categories': categories,
            'MRP': mrp,
            'stock_picking': stock_picking,
            # 'stock_inventory': stock_inventory,
            'stock_warehouse': stock_warehouse,
        }
        return vals

    def create_domain(self, model, record, move_type=None):
        domain = []

        if record.date_from:
            date_from = datetime.combine(fields.Date.from_string(record.date_from), time.min)
            domain.append(('create_date', '>=', fields.Datetime.to_string(date_from)))
        if record.date_to:
            date_to = datetime.combine(fields.Date.from_string(record.date_to), time.max)
            domain.append(('create_date', '<=', fields.Datetime.to_string(date_to)))

        if record.company_ids:
            domain.append(('company_id', 'in', record.company_ids.ids))
        if record.user_id:
            domain.append(('create_uid', '=', record.user_id.id))
        if move_type:
            domain.append(('move_type', '=', move_type))

        return self.env[model].sudo().search(domain)
