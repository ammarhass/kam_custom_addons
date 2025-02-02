# -*- coding: utf-8 -*-
{
    'name': "Vision Onboarding Report",

    'summary': """
        To add onboarding report report""",

    'description': """
        Long description of module's purpose
    """,
    'author': "Kam",
    'website': "http://www.yourcompany.com",
    'category': 'Hidden',
    'version': '16.0.0.1',
    'depends': ['hr' ,'mail'],
    'data': [
        'report/onboarding_template.xml',
        'report/onboarding_report.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install"': False,
    'application': True,
}