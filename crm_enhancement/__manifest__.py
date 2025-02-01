# -*- coding: utf-8 -*-
{
    'name': 'crm_enhancement',
    'version': '16.0',
    'category': 'base',
    'author': ' Mahmoud Fathi, mahmah273@gmail.com',
    'website': "https://www.linkedin.com/in/mahmoud-mohamed-096638110/",
    'license': 'LGPL-3',
    'summary': """
    Crm Enhancement
    """,
    'depends': [
        'base', 'crm',
    ],
    'data': [

        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/crm_lead.xml',
        'views/crm_stage.xml',
        # 'views/crm_lead_view.xml',

    ],

    'installable': True,
    'auto_install': False,
    'application': False
}
