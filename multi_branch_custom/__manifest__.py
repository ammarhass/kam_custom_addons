{
    'name': "Multi Branch Custom",

    'depends': ['base', 'account', 'stock_account', 'multi_branch_base'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_category_branch_account.xml',

    ],
}
