# -*- coding: utf-8 -*-
{
    'name': "POS Restaurant Receipt",

    'summary': """
        This module contains printing restaurants receipt whenever categories printer not connected.
        and restrict pos user to delete orders from pos screen.""",

    'description': """
        This module contains printing restaurants receipt whenever categories printer not connected.
        and restrict pos user to delete orders from pos screen.
    """,

    'author': "Khalid Shaheen",
    'website': "+201552520894",
    'depends': ['base', 'pos_restaurant'],
    'data': [
        'views/views.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            # 'sha_restaurant_receipt/static/src/xml/*.xml',
            # 'sha_restaurant_receipt/static/src/js/*.js',
            # ////////////////////////////////////////////////////////////////////////
            # 'sha_restaurant_receipt/static/src/xml/CaptainTemplateButton.xml',
            'sha_restaurant_receipt/static/src/xml/ResReceipt.xml',
            'sha_restaurant_receipt/static/src/xml/ResReceiptScreen.xml',
            'sha_restaurant_receipt/static/src/xml/TicketScreen.xml',
            # 'sha_restaurant_receipt/static/src/js/CaptainTemplateButton.js',
            'sha_restaurant_receipt/static/src/js/OrderlineCustomerNoteButton.js',
            'sha_restaurant_receipt/static/src/js/ProductScreen.js',
            'sha_restaurant_receipt/static/src/js/ResReceipt.js',
            'sha_restaurant_receipt/static/src/js/ResReceiptScreen.js',
            'sha_restaurant_receipt/static/src/js/RestaurantReceipt.js',
            'sha_restaurant_receipt/static/src/js/SubmitOrderButton.js',
        ],
    },
}
