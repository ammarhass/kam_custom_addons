odoo.define('sha_restaurant_receipt.models', function (require) {
"use strict";

const { Order } = require('point_of_sale.models');
const Registries = require('point_of_sale.Registries');
const core = require('web.core');
const Printer = require('point_of_sale.Printer').Printer;
const PosComponent = require('point_of_sale.PosComponent');
const QWeb = core.qweb;

const PosRestaurantOrderInherit = (Order) => class PosRestaurantOrderInherit extends Order {
    constructor(obj, options) {
        super(...arguments);
        this.order_change = [];
        this.captain = "";
    }

    async printChanges(){
        let isPrintSuccessful = true;
        const d = new Date();
        let hours = '' + d.getHours();
        hours = hours.length < 2 ? ('0' + hours) : hours;
        let minutes = '' + d.getMinutes();
        minutes = minutes.length < 2 ? ('0' + minutes) : minutes;

        for (const printer of this.pos.unwatched.printers) {
            const changes = this._getPrintingCategoriesChanges(printer.config.product_categories_ids);
            if (changes['new'].length > 0 || changes['cancelled'].length > 0) {

                const printingChanges = {
                    new: changes['new'],
                    cancelled: changes['cancelled'],
                    table_name: this.pos.config.iface_floorplan ? this.getTable().name : false,
                    floor_name: this.pos.config.iface_floorplan ? this.getTable().floor.name : false,
                    name: this.name || 'unknown order',
                    time: {
                        hours,
                        minutes,
                    },
                };
                if (!printer.config.proxy_ip){
                    this.order_change.push(printingChanges);
                    isPrintSuccessful = false;
                } else {
                    const receipt = QWeb.render('OrderChangeReceipt', { changes: printingChanges });
                    const result = await printer.print_receipt(receipt);
                    if (!result.successful) {
                        isPrintSuccessful = false;
                    }
                }
                //                this.order_change.push(printingChanges);
                //                const receipt = QWeb.render('OrderChangeReceipt', { changes: printingChanges });
                //                const result = await printer.print_receipt(receipt);
                //                if (!result.successful) {
                //                    isPrintSuccessful = false;
                //                }
            }
        }
       return isPrintSuccessful;
    }



}
    Registries.Model.extend(Order, PosRestaurantOrderInherit);


});