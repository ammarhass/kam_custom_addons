odoo.define('sha_default_accounts.RequiredPartner', function(require) {
    'use strict';

    const Registries = require('point_of_sale.Registries');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    var session = require('web.session');

     const RequiredPartner = (PaymentScreen) => class extends PaymentScreen {

        async _isOrderValid(isForceValidate) {

            if (!this.currentOrder.get_partner()) {
                const { confirmed } = await this.showPopup('ConfirmPopup', {
                    title: this.env._t('Customer Required'),
                    body: _.str.sprintf(this.env._t('Customer is required.')),
                });
                if (confirmed) {
                    this.selectPartner();
                }
                return false;
            }

            return super._isOrderValid(isForceValidate)
        }

    }

     Registries.Component.extend(PaymentScreen, RequiredPartner);
     return RequiredPartner;
});
