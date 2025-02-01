
{
    'name': 'Report Log',
    'version': '15.0',
    'category': 'Others',
    'summary': 'Generates log record each time a report is printed.',
    'description': """Generates log record each time a report is printed.""",
    'depends': ['web'],
    'author': 'OdooBot',
    'license': 'LGPL-3',
    'website': 'odoobot.8069@gmail.com',
    'price': 0,
	'currency': "EUR",
    'images': [
        'static/src/img/screenshot.png',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/report_log_security.xml',
        'views/ir_report_views.xml',
        'views/report_log_views.xml',
    ],
    'application': False,
}
