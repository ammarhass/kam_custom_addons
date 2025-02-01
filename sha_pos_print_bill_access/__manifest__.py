# -*- coding: utf-8 -*-
{
    'name': "POS Print Bill Access",

    'summary': """This module contains preventing pos user from printing bill before pressing order button. """,

    'description': """
        This module contains preventing pos user from printing bill before pressing order button. 
    """,

    'author': "Khalid Shaheen",
    'website': "+201552520894",
    'depends': ['base', 'sha_restaurant_receipt'],
    'data': [
        'views/views.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'sha_pos_print_bill_access/static/src/js/*.js',
            'sha_pos_print_bill_access/static/src/xml/TableWidget.xml',
            'sha_pos_print_bill_access/static/src/xml/ProductScreen.xml',
        ],
    },
}
