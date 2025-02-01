odoo.define("sha_default_accounts.partner_list", function (require) {
    "use strict";

    const PartnerListScreen = require("point_of_sale.PartnerListScreen");
    const Registries = require("point_of_sale.Registries");
    const { onMounted, onWillUnmount, useRef } = owl;

    const PartnerListScreenInherit = (PartnerListScreen) => class extends PartnerListScreen {

            async saveChanges(event) {

                let rec_id = this.env.pos.config.default_account_receivable_id
                let pay_id = this.env.pos.config.default_account_payable_id
                let property_account_receivable_id = rec_id ?  rec_id[0] : false;
                let property_account_payable_id = pay_id ? pay_id[0] : false;
                var processedChanges = event.detail.processedChanges
                processedChanges['property_account_receivable_id'] = property_account_receivable_id
                processedChanges['property_account_payable_id'] = property_account_payable_id

                if ((processedChanges['name'].trim()).length < 7 ){

                    this.showPopup('ErrorPopup', {
                        title: this.env._t('Error'),
                        body: this.env._t('Name must be greater than 7 characters.')
                     });
                    return;

                }
                var pattern = /^01[0125][0-9]{8}$/gm
                let match = pattern.test(processedChanges['mobile'].trim())
                if (!processedChanges['mobile'].trim() || !match){
                    this.showPopup('ErrorPopup', {
                        title: this.env._t('Error'),
                        body: this.env._t('Please enter a valid mobile.')
                    });
                    return;

                }


                try {
                    let partnerId = await this.rpc({
                        model: 'res.partner',
                        method: 'create_from_ui',
                        args: [event.detail.processedChanges],
                    });
                    await this.env.pos._loadPartners([partnerId]);
                    this.state.selectedPartner = this.env.pos.db.get_partner_by_id(partnerId);
                    this.confirm();
                } catch (error) {
                    if (isConnectionError(error)) {
                        await this.showPopup('OfflineErrorPopup', {
                            title: this.env._t('Offline'),
                            body: this.env._t('Unable to save changes.'),
                        });
                    } else {
                        throw error;
                    }
                }
            }

        };

    Registries.Component.extend(PartnerListScreen, PartnerListScreenInherit);
});
