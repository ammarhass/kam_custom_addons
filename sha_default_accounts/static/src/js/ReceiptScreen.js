/** @odoo-module **/

import Registries from 'point_of_sale.Registries';
import ReceiptScreen from 'point_of_sale.ReceiptScreen';

const ReceiptScreenInherit = (ReceiptScreen) => { class ReceiptScreenInherit extends ReceiptScreen {

        async printReceipt() {
            //console.log("printReceipt1");
            await super.printReceipt();
            //console.log("printReceipt2");
            this.orderDone()
        }

    }
    return ReceiptScreenInherit;
};
Registries.Component.extend(ReceiptScreen, ReceiptScreenInherit);

