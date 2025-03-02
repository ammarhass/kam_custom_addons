# -*- coding: utf-8 -*-
{
    'name': "Vision Employee Details Custom",

    'summary': """
        To add new report to Hr Employee""",

    'description': """
        Long description of module's purpose
    """,
    'author': "Kam",
    'website': "http://www.yourcompany.com",
    'category': 'Hidden',
    'version': '16.0.0.1',
    'depends': ['hr'],
    'data': [
        'security/ir.model.access.csv',
        'report/employee_details_template.xml',
        'report/employee_details_report.xml',
        'views/promotion_details_views.xml',
        'views/device_equipment_details_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install"': False,
    'application': True,
}