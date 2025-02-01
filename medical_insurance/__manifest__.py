# -*- coding: utf-8 -*-
{
    'name': "Medical Insurance Details",

    'summary': """
        Medical Insurance Details""",

    'description': """
        Long description of module's purpose
    """,
    'author': "Kam",
    'website': "http://www.yourcompany.com",
    'category': 'Hidden',
    'version': '16.0.0.1',
    'depends': ['hr', 'mail', 'hr_contract'],
    'data': [
        'security/ir.model.access.csv',
        'views/medical_insurance_views.xml',
        'views/hr_contract_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install"': False,
    'application': True,
}