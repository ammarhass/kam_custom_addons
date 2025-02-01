odoo.define('sha_restaurant_receipt.OrderlineCustomerNoteButtonInherit', function(require) {
    'use strict';

    const OrderlineCustomerNoteButton = require('point_of_sale.OrderlineCustomerNoteButton');
    const Registries = require('point_of_sale.Registries');

    const OrderlineCustomerNoteButtonInherit = (OrderlineCustomerNoteButton) =>
        class extends OrderlineCustomerNoteButton {
            setup() {
                super.setup();
            }

            async onClick() {
                const selectedOrderline = this.env.pos.get_order().get_selected_orderline();
                if (!selectedOrderline) return;

                const { confirmed, payload: inputNote } = await this.showPopup('TextAreaPopup', {
                    startingValue: selectedOrderline.get_customer_note(),
                    title: this.env._t('Add Customer Note'),
                });

                if (confirmed) {
                    selectedOrderline.set_note(inputNote);
                }
            }


        };

    Registries.Component.extend(OrderlineCustomerNoteButton, OrderlineCustomerNoteButtonInherit);

    return OrderlineCustomerNoteButton;
});
