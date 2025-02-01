odoo.define('sha_restaurant_receipt.SubmitOrderButton', function(require) {
    'use strict';

    const SubmitOrderButton = require('pos_restaurant.SubmitOrderButton');
    const Registries = require('point_of_sale.Registries');

    const SubmitOrderButtonInherit = (SubmitOrderButton) =>
        class extends SubmitOrderButton {
            setup() {
                super.setup();
            }

            async _onClick() {
                if (!this.clicked) {
                    try {
                        this.clicked = true;
                        const order = this.env.pos.get_order();
                        if (order.hasChangesToPrint()) {

                            const isPrintSuccessful = await order.printChanges();
                            if (isPrintSuccessful) {
                                order.updatePrintedResume();
                            } else {
                                await this.showTempScreen('ResReceiptScreen');
                                order.updatePrintedResume();
                                order.order_change = [];
                            }

                        }
                    } finally {
                        this.clicked = false;
                    }
                }
            }


        };

    Registries.Component.extend(SubmitOrderButton, SubmitOrderButtonInherit);

    return SubmitOrderButton;
});
