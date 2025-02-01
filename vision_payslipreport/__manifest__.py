# -*- coding: utf-8 -*-
{
    'name': "Vision Payslip Report",

    'summary': """
        To add customization to payslip report""",

    'description': """
        Long description of module's purpose
    """,
    'author': "Kam",
    'website': "http://www.yourcompany.com",
    'category': 'Hidden',
    'version': '16.0.0.1',
    'depends': ['hr' ,'hr_payroll_community'],
    'data': [
        'report/report_payslipdetails_template.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install"': False,
    'application': True,
}