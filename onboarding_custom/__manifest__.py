# -*- coding: utf-8 -*-
{
    'name': "On Boarding Custom",

    'summary': """
        To manage the On Boarding Plan""",

    'description': """
        Long description of module's purpose
    """,
    'author': "Kam",
    'website': "http://www.yourcompany.com",
    'category': 'Hidden',
    'version': '16.0.0.1',
    'depends': ['hr', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/user_groups.xml',
        'views/hr_department_views.xml',
        'views/hr_employee_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install"': False,
    'application': True,
}