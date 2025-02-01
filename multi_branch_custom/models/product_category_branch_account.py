from odoo import models, fields

class ProductCategory(models.Model):
    _inherit = 'product.category'

    branch_account_ids = fields.One2many(
        'product.category.branch.account', 'category_id', string='Branch Accounts')

class ProductCategoryBranchAccount(models.Model):
    _name = 'product.category.branch.account'
    _description = 'Product Category Branch Account'

    category_id = fields.Many2one('product.category')
    branch_id = fields.Many2one('res.branch', string='Branch', required=True)
    expense_account_id = fields.Many2one('account.account', string='Expense Account')
    income_account_id = fields.Many2one('account.account', string='Income Account')
    property_stock_account_input_categ_id = fields.Many2one('account.account', string="Input Account for Stock Valuation")
    property_stock_account_output_categ_id = fields.Many2one('account.account', string="Output Account for Stock Valuation")
    property_stock_valuation_account_id = fields.Many2one('account.account', string="Account Template for Stock Valuation")
    property_stock_journal = fields.Many2one(
        'account.journal', 'Stock Journal', company_dependent=True,
        domain="[('company_id', '=', allowed_company_ids[0])]", check_company=True,
        help="When doing automated inventory valuation, this is the Accounting Journal in which entries will be automatically posted when stock moves are processed.")
