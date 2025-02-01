odoo.define('sha_restaurant_receipt.CaptainTemplateButton', function (require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');
    const { useListener } = require("@web/core/utils/hooks");
    const core = require('web.core');
    const _t = core._t;
    const { Gui } = require('point_of_sale.Gui');

    class CaptainTemplateButton extends PosComponent {
        setup() {
            useListener('click', this._onClick);
        }

        async _onClick() {
            const { confirmed, payload: inputNote } = await this.showPopup('TextAreaPopup', {
                //startingValue: selectedOrderline.get_customer_note(),
                title: this.env._t('Add Customer Note'),
            });

            if (confirmed) {
                let order = this.env.pos.get_order()
                //console.log('inputNote: ', inputNote);
                order.captain = inputNote
            }
        }
    }
    CaptainTemplateButton.template = 'CaptainTemplateButton';
    ProductScreen.addControlButton({
      // Add button in product screen
        component: CaptainTemplateButton,
        condition: function () {
            return true;
        },
    });
    Registries.Component.add(CaptainTemplateButton);
    return CaptainTemplateButton;
});
