# -*- coding: utf-8 -*-
{
    'name': 'sales_enhancement',
    'version': '16.0',
    'category': 'base',
    'author': ' Mahmoud Fathi, mahmah273@gmail.com',
    'website': "https://www.linkedin.com/in/mahmoud-mohamed-096638110/",
    'license': 'LGPL-3',
    'summary': """
    sales enhancement 
    """,
    'depends': [
        'base', 'sale',
    ],
    'data': [

        'views/sale_order_view.xml',

    ],

    'installable': True,
    'auto_install': False,
    'application': False
}
