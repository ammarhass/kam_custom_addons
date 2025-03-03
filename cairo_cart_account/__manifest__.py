# -*- coding: utf-8 -*-
{
    'name': 'CairoCart Accounting ',
    'version': '16.0',
    'category': 'base',
    'author': 'Zad Solutions, Mahmoud Fathi, Mohamed Tarek',
    'website': "http://zadsolutions.com",
    'summary': """
    CairoCart Accounting 
    """,
    'depends': [
        'base', 'account', 'bi_sale_purchase_discount_with_tax'
    ],
    'data': [
        'views/account_move.xml',
        'report/invoice_report.xml',
        # 'views/account_payment_views.xml',
        # 'views/account_journal_views.xml',
        # 'views/branch_views.xml',
        # 'views/account_setting.xml'

    ],

    'installable': True,
    'auto_install': False,
    'application': False
}
