# -*- coding: utf-8 -*-
{
    'name': "Hr Requests",

    'summary': """
        To manage the hr requests""",

    'description': """
        Long description of module's purpose
    """,
    'author': "Kam",
    'website': "http://www.yourcompany.com",
    'category': 'Hidden',
    'version': '16.0.0.1',
    'depends': ['hr', 'mail', 'equipment_request_it_operations'],
    'data': [
        'security/ir.model.access.csv',
        'security/user_groups.xml',
        'views/hr_requests_views.xml',
        'views/menus.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install"': False,
    'application': True,
}