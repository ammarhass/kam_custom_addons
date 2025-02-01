{
    "name": "Accounting Updates",
    "depends": ["base", "account", "payment", "invoice_stock_move", "stock", "sale", "purchase", "stock_account", "accounting_pdf_reports"],

    "data": [
        "security/ir.model.access.csv",
        "security/audit_groups.xml",
        "wizard/journal_entry_wizard_view.xml",
        'views/inherit_account_account_form_view.xml',
        "views/account_journal_form_view.xml",
        "views/journal_form_move_view.xml",
        "views/inherit_view_account_move_line_filter.xml",
        "data/server_actions.xml",
        "data/audit_note_data.xml",
    ],

    "author": "",
    "description": "containing custom updates for accounting module",
}
