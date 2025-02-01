odoo.define('sha_pos_print_bill_access.FloorScreen', function(require) {
    'use strict';

    const FloorScreen = require('pos_restaurant.FloorScreen');
    const Registries = require('point_of_sale.Registries');
    const { isConnectionError } = require('point_of_sale.utils');
    const { onWillStart } = owl;

    const FloorScreenInherit = (FloorScreen) => class extends FloorScreen {

        setup() {
            super.setup();
            onWillStart(async () => {
                //console.log("onWillStart");
                let activeTables = this.activeFloor.tables
                for (const table of activeTables){
                    await this.isOrderBilled(table)
                }
            });
        }

        async onPatched() {
            //console.log("onPatched");
            this.floorMapRef.el.style.background = this.state.floorBackground;
            this.state.floorMapScrollTop = this.floorMapRef.el.getBoundingClientRect().top;
            let activeTables = this.activeFloor.tables
            for (const table of activeTables){
                await this.isOrderBilled(table)
            }
        }

        ///////////////////////////////////////////////////////////////////////////////////////////////////

        async isOrderBilled(table) {
            let tablOrders = this.env.pos.getTableOrders(table.id)
            //console.log("tablOrders: ", tablOrders);
            if (tablOrders.length == 0){
                table.billed = false
            } else if (tablOrders.length > 0){
                let domain = [['pos_reference', '=', tablOrders[0].name]]
                let res = await this.rpc({
                    model: 'pos.order',
                    method: 'search_read',
                    kwargs: {
                        domain: domain,
                        fields: ['is_printed'],
                    },
                });
                //console.log("Res: ", res);
                let is_printed = res.length > 0 ? res[0]['is_printed'] : false;
                //console.log("is_printed: ", is_printed);
                table.billed = is_printed
            }
            return table.billed
        }

        //        //////////////////////////////////////////////////////////////////

        //        async isOrderBilled(table) {
        //            console.log("////////////////////////////////////////////////////////////////");
        //            let tablOrders = this.env.pos.getTableOrders(table.id)
        //            if (table.id === 30){
        //                console.log("Table1: ", table);
        //                console.log("table_id: ", table.id);
        //                console.log("tablOrders: ", tablOrders);
        //            }
        //            if (tablOrders.length == 0){
        //                console.log("If")
        //                table.billed = false
        //            } else if (tablOrders.length > 0 && tablOrders[0].printingChanges['cancelled'].length===0 && tablOrders[0].printingChanges['new'].length===0){
        //                console.log("Else If")
        //                //console.log("1: ", tablOrders[0].printingChanges['cancelled']);
        //                //console.log("2: ", tablOrders[0].printingChanges['cancelled'].length===0);
        //                //console.log("2: ", !tablOrders[0].printingChanges['new']);
        //                table.billed = true
        //            }
        //            console.log("Table2: ", table);
        //            return table.billed
        //        }

        async onSelectTable(table) {
            //console.log("////////////////////////////////////////////////");
            //console.log("1")
            if (this.state.isEditMode) {
                //console.log("2")
                this.state.selectedTableId = table.id;
            } else {
                //console.log("3")
                try {
                    if (this.env.pos.orderToTransfer) {
                        //console.log("4")
                        await this.env.pos.transferTable(table);
                    } else {
                        //console.log("5")
                        await this.env.pos.setTable(table);
                    }
                } catch (error) {
                    //console.log("6")
                    if (isConnectionError(error)) {
                        await this.showPopup('OfflineErrorPopup', {
                            title: this.env._t('Offline'),
                            body: this.env._t('Unable to fetch orders'),
                        });
                    } else {
                        throw error;
                    }
                }
                const order = this.env.pos.get_order();
                //console.log("7")
                if (order.get_orderlines().length === 0){
                    //console.log("8")
                    this.env.pos.removeOrder(order);
                }
                this.showScreen(order.get_screen_data().name);
                //console.log("9")
            }
        }

        get activeTables() {
            return this.activeFloor.tables;
        }

    };

    Registries.Component.extend(FloorScreen, FloorScreenInherit);

    return FloorScreen;
});
