# -*- coding: utf-8 -*-
{
    'name': 'accounting_enhancement',
    'version': '16.0',
    'category': 'account',
    'author': ' Mahmoud Fathi, mahmah273@gmail.com',
    'website': "https://www.linkedin.com/in/mahmoud-mohamed-096638110/",
    'license': 'LGPL-3',
    'summary': """
    accounting_enhancement
    """,
    'depends': [
      'accounting_pdf_reports','bi_sale_purchase_discount_with_tax','stock', 'account', 'sale', 'purchase'
    ],
    'data': [

        # 'security/ir.model.access.csv',
        'security/res_groups.xml',
        'data/server_action.xml',
        'report/purchase_template.xml',
        'views/company_view.xml',
        'report/invoice_report.xml',
        'report/journal_entry_report.xml',
        'report/sale_template.xml',
        'report/payment_template.xml',
        'report/picking_report.xml',

    ],
    # 'assets': {
    #     'web.report_assets_common': [
    #         'accounting_enhancement/static/src/img/newgdara.jpeg',
    #     ],
    # },

    'installable': True,
    'auto_install': False,
    'application': False
}
