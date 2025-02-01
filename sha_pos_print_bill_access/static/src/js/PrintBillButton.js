odoo.define('sha_pos_print_bill_access.PrintBillButton', function(require) {
    'use strict';

    const PrintBillButton = require('pos_restaurant.PrintBillButton');
    const Registries = require('point_of_sale.Registries');

    const PrintBillButtonInherit = (PrintBillButton) =>
        class extends PrintBillButton {
            setup() {
                super.setup();
                //console.log('PrintBillButton: ', this);
            }

            async onClick() {
                const order = this.env.pos.get_order();
                let printingChanges = order.printingChanges
                var valid = true;
                for (const key in printingChanges) {
                    if (printingChanges[key].length > 0){
                        valid = false;
                        break;
                    }
                }
                if (!valid){
                    await this.showPopup('ErrorPopup', {
                        title: this.env._t('Print Bill Invalid'),
                        body: this.env._t('You cannot print bill without pressing order button.'),
                    });
                } else {
                    super.onClick();
                    await this.rpc({
                        model: 'pos.order',
                        method: 'set_table_is_printed',
                        args: [false, order.name],
                    });
                }
            }
        };

    Registries.Component.extend(PrintBillButton, PrintBillButtonInherit);

    return PrintBillButton;
});
