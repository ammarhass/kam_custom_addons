# -*- coding: utf-8 -*-
{
    'name': 'Inventory Enhancement',
    'version': '16.0',
    'category': 'base',
    'author': 'Zad Solutions, Mahmoud Fathi',
    # 'website': "http://zadsolutions.com",
    'summary': """
    Inventory Enhancements 
    """,
    'depends': [
        'base',  'stock',
    ],
    'data': [

        # 'security/group_security.xml',
        'security/ir.model.access.csv',
        # 'views/stock_landed_cost.xml',
        # 'views/stock_picking.xml',
        # 'views/stock_return_picking.xml',
        # 'views/stock_scrap.xml',
        # 'views/stock_move_line.xml',
        'wizard/auto_carrier.xml',
        'data/server_action.xml',

    ],

    'installable': True,
    'auto_install': False,
    'application': False
}
