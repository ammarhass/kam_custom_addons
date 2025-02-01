{
    "name": "Product Custom",
    "depends": ["base", "product", "purchase", "stock_account"],

    "data": [
        'security/ir.model.access.csv',
        # 'views/product_test.xml',
        'views/product_supplierifo_inherit_view.xml',
        'views/inherit_purchase_order_form_view.xml',
        'wizard/compute_fields_average_view.xml',
        'wizard/create_unbuild_order_view.xml',
    ],

    "author": "",
    "description": "",
}
