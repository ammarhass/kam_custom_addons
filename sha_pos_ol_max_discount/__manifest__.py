# -*- coding: utf-8 -*-
{
    'name': "POS Order Lines max Discount",

    'summary': """This module contains adding max discount at POS order lines.""",

    'description': """
        This module contains adding max discount at POS order lines.
    """,

    'author': "Khalid Shaheen",
    'website': "+201552520894",
    'depends': ['base', 'point_of_sale', 'sha_restaurant_receipt'],
    'data': [
        'views/views.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'sha_pos_ol_max_discount/static/src/js/ProductScreen.js',
        ],
    },
}
