# -*- coding: utf-8 -*-
{
    'name': "User Activities",

    'summary': """
        Create report for all user activities.
        """,

    'category': 'HR',
    'version': '1.1.2',

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'wizard/user_activity_report.xml',
        'wizard/user_activity_report_template.xml',
    ],

}
