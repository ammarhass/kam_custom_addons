odoo.define('sha_restaurant_receipt.ResReceipt', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    class ResReceipt extends PosComponent {
          /**
            * @Override PosComponent
          */
         setup() {
            super.setup();
            this.all_changes = this.props.order_changes
            this.order_captain = this.props.order_captain
        }
        get order_changes() {
            return this.all_changes;
        }
        get captain() {
            return this.order_captain;
        }
    }
    ResReceipt.template = 'ResReceipt';
    Registries.Component.add(ResReceipt);
    return ResReceipt;
});
