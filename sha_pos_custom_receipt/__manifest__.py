# -*- coding: utf-8 -*-
{
    'name': 'POS Custom Receipt',
    'category': 'Sales/Point of Sale',
    'summary': 'This module is used to customized receipt of point of sale when a user adds a product in the cart and validates payment and print receipt, then the user can see the client name on POS Receipt. | Custom Receipt | POS Reciept | Payment | POS Custom Receipt',
    'description': "Customized our point of sale receipt",
    # 'version': '16.0.1.0',
    # 'website': 'https://www.sysgates.com',
    'author': 'Khalid Shaheen',
    # 'images': ['static/description/banner.jpg'],
    'depends': ['base', 'point_of_sale', 'total_quantity_pos'],
    'data': [
        # 'views/views.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            # "sha_pos_custom_receipt/static/css/style.css",
            # "sha_pos_custom_receipt/static/src/js/models.js",
            # "sha_pos_custom_receipt/static/src/js/OrderReceipt.js",
            "sha_pos_custom_receipt/static/src/xml/pos.xml",
            "sha_pos_custom_receipt/static/src/xml/ClosePosPopup.xml",
        ],
    },
}
