/** @odoo-module **/

import ProductScreen from 'point_of_sale.ProductScreen';
const PosComponent = require('point_of_sale.PosComponent');
const ControlButtonsMixin = require('point_of_sale.ControlButtonsMixin');
const NumberBuffer = require('point_of_sale.NumberBuffer');
const { useListener } = require("@web/core/utils/hooks");
const Registries = require('point_of_sale.Registries');
const { useBarcodeReader } = require('point_of_sale.custom_hooks');
const { isConnectionError } = require('point_of_sale.utils');
const { parse } = require('web.field_utils');
const core = require('web.core');
const _t = core._t;
const { Gui } = require('point_of_sale.Gui');

const { onMounted, useState } = owl;

export const MaxDiscount = (ProductScreen) => class extends ProductScreen {

        setup() {
            super.setup();
        }

        async _updateSelectedOrderline(event) {
            var orderline = this.env.pos.selectedOrder.selected_orderline;
            if (orderline) {
                var oldDiscount = orderline.discount;
                await super._updateSelectedOrderline(event);  // Call super method once

                var newDiscount = orderline.discount;
                var maxDiscount = this.env.pos.company.ol_max_discount * 100;

                if (newDiscount > maxDiscount) {
                    orderline.discount = oldDiscount;  // Revert to old discount
                    orderline.discountStr = oldDiscount.toString();  // Reset discount string
                    NumberBuffer.reset();  // Reset the numpad buffer

                    // Show error popup
                    return this.showPopup("ErrorPopup", {
                        title: this.env._t("Max Discount"),
                        body: this.env._t(`You cannot apply a discount more than ${maxDiscount}%`),
                    });
                }
	    }
	}

    };

Registries.Component.extend(ProductScreen, MaxDiscount);
