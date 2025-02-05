# -*- coding: utf-8 -*-
{
    'name': "POS Orders Access",

    'summary': """This module add access to pos orders.""",

    'description': """
        This module add access to pos orders.
    """,

    'author': "Khalid Shaheen",
    'website': "+201552520894",
    'depends': ['base', 'point_of_sale'],
    'data': [
        'views/views.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'sha_pos_orders_access/static/src/xml/TicketButton.xml',
        ]
    }
}
