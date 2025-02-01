{
    'name': "Contact Custom",

    'depends': ['base', 'crm', 'sale', 'purchase', 'account'],
    'data': [
            'views/res_partner.xml',
            'views/account_move_form_view.xml',
            # 'views/sale_order_form_view.xml',
            # 'views/purchase_order_form_view.xml',
    ],
}
