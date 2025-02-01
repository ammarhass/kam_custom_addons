{
    "name": "Fiberone Reports Custom",
    "depends": ["base", "product", "purchase", "stock_account", "stock", "sale"],

    "data": [
        # 'security/ir.model.access.csv',
        'report/report_purchasequotation_inherit.xml',
        'report/report_purchaseorder_inherit.xml',
        'report/report_deliveryslip_inherit.xml',
        'report/report_stockpicking_operations_inherit.xml',
        'report/report_invoice_document_inherit.xml',
        'report/report_saleorder_document_inherit.xml',
    ],

    "author": "",
    "description": "",
}