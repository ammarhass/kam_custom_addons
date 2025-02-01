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

export const LockPriceDiscount = (ProductScreen) =>
    class extends ProductScreen {
        setup() {
            super.setup();
        }

        async _updateSelectedOrderline(event) {
            const order = this.env.pos.get_order();
            const selectedLine = order.get_selected_orderline();
            if (selectedLine && selectedLine.isTipLine() && this.env.pos.numpadMode !== "price") {
                NumberBuffer.reset();
                if (event.detail.key === "Backspace") {
                    console.log("This: ", this);
                    this._setValue("remove");
                } else {
                    this.showPopup("ErrorPopup", {
                        title: this.env._t("Cannot modify a tip"),
                        body: this.env._t("Customer tips, cannot be modified directly"),
                    });
                }
            } else if (this.env.pos.numpadMode === 'quantity' && this.env.pos.disallowLineQuantityChange()) {
                if(!order.orderlines.length)
                    return;
                let orderlines = order.orderlines;
                let lastId = orderlines.length !== 0 && orderlines.at(orderlines.length - 1).cid;
                let currentQuantity = this.env.pos.get_order().get_selected_orderline().get_quantity();

                if(selectedLine.noDecrease) {
                    this.showPopup('ErrorPopup', {
                        title: this.env._t('Invalid action'),
                        body: this.env._t('You are not allowed to change this quantity'),
                    });
                    return;
                }
                const parsedInput = event.detail.buffer && parse.float(event.detail.buffer) || 0;
                if(lastId != selectedLine.cid)
                    this._showDecreaseQuantityPopup();
                else if(currentQuantity < parsedInput)
                    this._setValue(event.detail.buffer);
                else if(parsedInput < currentQuantity)
                    this._showDecreaseQuantityPopup();
            } else {
                let { buffer } = event.detail;
                let val = buffer === null ? 'remove' : buffer;
                ///////////////////////////////////////////////////////////////////////////////////////////////
                if (!this.env.pos.config.delete_allowed){

                    if (event.detail.key === "Backspace") {
                        let order = this.env.pos.selectedOrder
                        let order_line = this.env.pos.selectedOrder.selected_orderline
                        let product_id = order_line.product.id
                        let printedResume = order.printedResume
                        let line_printed = false;

                        for (const property in printedResume) {
                            let printed_obj = printedResume[property]
                            if (printed_obj.product_id === product_id){
                                line_printed = true;
                                break;
                            }
                        }

                        if (line_printed){
                            this.showPopup("ErrorPopup", {
                                title: this.env._t("Delete Line"),
                                body: this.env._t("Cannot delete this line because it's already printed."),
                            });
                        } else {
                            this._setValue(val);
                            if (val == 'remove') {
                                NumberBuffer.reset();
                                this.env.pos.numpadMode = 'quantity';
                            }
                        }

                    } else{
                    	debugger
                        let order = this.env.pos.selectedOrder
                        let order_line = this.env.pos.selectedOrder.selected_orderline
                        let product_id = order_line.product.id
                        let printedResume = order.printedResume
                        let line_printed = false;

                        for (const property in printedResume) {
                            let printed_obj = printedResume[property]
                            if (printed_obj.product_id === product_id){
                                line_printed = true;
                                break;
                            }
                        }

                        if (line_printed){
                            this.showPopup("ErrorPopup", {
                                title: this.env._t("Edit Line"),
                                body: this.env._t("Cannot Edit this line because it's already printed."),
                            });
                        } else {
                            this._setValue(val);
                            if (val == 'remove') {
                                NumberBuffer.reset();
                                this.env.pos.numpadMode = 'quantity';
                            }
                        }

                    }
                    //                    else {
                    //                        console.log("Else");
                    //                        this._setValue(val);
                    //                        if (val == 'remove') {
                    //                            NumberBuffer.reset();
                    //                            this.env.pos.numpadMode = 'quantity';
                    //                        }
                    //                    }

                } else {
                    this._setValue(val);
                    if (val == 'remove') {
                        NumberBuffer.reset();
                        this.env.pos.numpadMode = 'quantity';
                    }
                }

            }
        }
    };

Registries.Component.extend(ProductScreen, LockPriceDiscount);
