odoo.define("sha_default_accounts.partner_list", function (require) {
    "use strict";

    const PartnerListScreen = require("point_of_sale.PartnerListScreen");
    const Registries = require("point_of_sale.Registries");
    const { onMounted, onWillUnmount, useRef } = owl;

    const PartnerListScreenInherit = (PartnerListScreen) => class extends PartnerListScreen {

        async searchForPartners(phone) {
            let domain = [];
            const limit = 30;
            const search_fields = [
                    "name",
                    "parent_name",
                    "phone_mobile_search",
                    "email",
                    "vat",
                ];
            domain = [
                ...Array(search_fields.length - 1).fill('|'),
                ...search_fields.map(field => [field, "ilike", phone + "%"])
            ];
            const result = await this.env.services.rpc(
                {
                    model: 'pos.session',
                    method: 'get_pos_ui_res_partner_by_params',
                    args: [
                        [odoo.pos_session_id],
                        {
                            domain,
                            limit: limit,
                            offset: this.state.currentOffset,
                        },
                    ],
                    context: this.env.session.user_context,
                },
                {
                    timeout: 3000,
                    shadow: true,
                }
            );
            return result;
        }

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

            let phone = processedChanges['mobile'].trim();
            let oldPartner = await this.searchForPartners(phone)
            if (oldPartner.length > 0){
                this.showPopup('ErrorPopup', {
                        title: this.env._t('Error'),
                        body: this.env._t('Mobile number is already linked to other customer.')
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
