{
    "name": "Arkad Excel Reprot",
    "depends": ["base", "account", "analytic", "product_custom", "stock"],

    "data": [
        'security/ir.model.access.csv',
        'security/res_groups.xml',
        'views/inherit_analytic_account.xml',
        'views/account_move_views.xml',
        'views/account_account_views.xml',
        'report/invoice_report.xml',
        # 'report/fix_inve.xml',
        'wizard/analytic_excel_wizard_views.xml',
        'wizard/vendor_excel_wizard_view.xml',
    ],

    "author": "",
    "description": "",
}