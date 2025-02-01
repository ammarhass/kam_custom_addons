# -*- coding: utf-8 -*-
{
    'name': "POS Default Paypal/Receivable Accounts",

    'summary': """POS Default Paypal/Receivable Accounts""",

    'description': """
        POS Default Paypal/Receivable Accounts
    """,

    'author': "Khalid Shaheen",
    'website': "201552520894",
    'depends': ['base', 'point_of_sale'],

    'data': [
        'views/views.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'sha_default_accounts/static/src/js/PartnerList.js',
            'sha_default_accounts/static/src/js/ReceiptScreen.js',
            'sha_default_accounts/static/src/js/RequiredPartner.js',
        ],
    },
}
