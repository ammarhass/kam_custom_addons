{
    "name": "Pearl Sale Order",
    "depends": ["base", "account", "product", "sale", "stock"],

    "data": [
        # 'security/ir.model.access.csv',
        'security/user_group.xml',
        'data/server_action.xml',
        'data/ir_cron.xml',
        'views/sale_order_line_views.xml',
        'views/sale_order_views.xml',
        'views/account_move_line_view.xml',
        'views/product_template_form_view.xml',
        'views/account_invoice_report_views.xml',
        'views/purchase_order_view.xml',
        'report/request_for_quotation.xml',
        'report/report_invoice.xml',
        'report/sale_report.xml',
        'report/purchase_order.xml',
        'report/stock_picking_report.xml',
        'report/delivery_slip.xml',
    ],

    "author": "",
    "description": "",
}
