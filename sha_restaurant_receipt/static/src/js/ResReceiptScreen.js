odoo.define('sha_restaurant_receipt.ResReceiptScreen', function (require) {
    'use strict';

    const { useRef } = owl;
    const Registries = require('point_of_sale.Registries');
    const AbstractReceiptScreen = require('point_of_sale.AbstractReceiptScreen');

    const ResReceiptScreen = (AbstractReceiptScreen) => { class ResReceiptScreen extends AbstractReceiptScreen {
            setup() {
                super.setup();
                this.all_changes = this.env.pos.get_order().order_change;
                this.order_captain = this.env.pos.get_order().captain;
            }
            confirm() {
                this.props.resolve({ confirmed: true, payload: null });
                this.trigger('close-temp-screen');
            }
            async printReceipt() {
                await this._printReceipt();
                this.confirm()
            }
            get changes(){
                return this.all_changes
            }
            get captain(){
                return this.order_captain
            }
        }
        ResReceiptScreen.template = 'ResReceiptScreen';
        return ResReceiptScreen;
    };
    Registries.Component.addByExtending(ResReceiptScreen, AbstractReceiptScreen);
    return ResReceiptScreen;
});