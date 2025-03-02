# -*- coding: utf-8 -*-
{
    'name': "POS new order",

    'summary': """POS go to new order after print receipt.""",

    'description': """
        POS go to new order after print receipt.
    """,

    'author': "Khalid Shaheen",
    'website': "201552520894",
    'depends': ['base', 'point_of_sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'sha_default_accounts/static/src/js/ReceiptScreen.js',
        ],
    },
}
