# -*- coding: utf-8 -*-
{
    'name': "Custody Customization",

    'summary': """
        To add customization to custody module""",

    'description': """
        Long description of module's purpose
    """,
    'author': "Kam",
    'website': "http://www.yourcompany.com",
    'category': 'Hidden',
    'version': '16.0.0.1',
    'depends': ['tt_hr_lib', 'hr', 'mail'],
    'data': [
        'data/custody_emails.xml',
        'views/hr_employee_views.xml',
        'views/custody_request_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install"': False,
    'application': True,
}