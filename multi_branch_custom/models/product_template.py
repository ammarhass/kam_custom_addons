from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _get_product_accounts(self):
        result = super(ProductTemplate, self)._get_product_accounts()
        branch_id = self.env.context.get('branch_id', False)
        if branch_id:
            branch_account = self.categ_id.branch_account_ids.filtered(lambda b: b.branch_id.id == branch_id.id)
            if branch_account:
                result= {
                    'income': branch_account.income_account_id,
                    'expense': branch_account.expense_account_id
                }
                result.update({
                    'stock_input':  branch_account.property_stock_account_input_categ_id,
                    'stock_output': branch_account.property_stock_account_output_categ_id,
                    'stock_valuation': branch_account.property_stock_valuation_account_id or False,
                })
        return result

    def get_product_accounts(self, fiscal_pos=None):
        """ Add the stock journal related to product to the result of super()
        @return: dictionary which contains all needed information regarding stock accounts and journal and super (income+expense accounts)
        """
        accounts = super(ProductTemplate, self).get_product_accounts(fiscal_pos=fiscal_pos)
        branch_id = self.env.context.get('branch_id', False)
        if branch_id:
            branch_account = self.categ_id.branch_account_ids.filtered(lambda b: b.branch_id.id == branch_id.id)
            if branch_account:
                accounts.update({'stock_journal': branch_account.property_stock_journal or False})
        return accounts

