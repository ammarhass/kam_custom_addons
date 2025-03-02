# -*- coding: utf-8 -*-
{
    'name' : 'Owl Tutorial',
    'version' : '1.0',
    'summary': 'OWL Tutorial',
    'sequence': -1,
    'description': """OWL Tutorial Custom Dashboard""",
    'category': 'OWL',
    'depends' : ['base', 'web', 'sale', 'board','account'],
    'data': [
        'views/sales_dashboard.xml',
        'views/account.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'odoo_custom_dashboard/static/src/components/**/*.js',
            'odoo_custom_dashboard/static/src/components/**/*.xml',
            'odoo_custom_dashboard/static/src/components/**/*.scss',
        ],
    },
}
