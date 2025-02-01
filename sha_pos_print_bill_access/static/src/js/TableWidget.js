odoo.define('sha_pos_print_bill_access.TableWidget', function(require) {
    'use strict';

    const TableWidget = require('pos_restaurant.TableWidget');
    const Registries = require('point_of_sale.Registries');
    const { onWillStart } = owl;

    const TableWidgetInherit = (TableWidget) => class extends TableWidget {

            setup() {
                super.setup();
                //                onWillStart(async () => {
                //                    let table = this.props.table
                //                    return await this.isOrderBilled(table);
                //                });
            }

            //            async isOrderBilled(table) {
            //                //console.log("////////////////////////////////////////////////////////////////");
            //                if (table.billed){
            //                    return table.billed;
            //                }
            //                let tablOrders = this.env.pos.getTableOrders(table.id)
            //                //console.log("table: ", table);
            //                if (tablOrders.length == 0){
            //                    table.billed = false
            //                } else if (tablOrders.length > 0){
            //                    let domain = [['pos_reference', '=', tablOrders[0].name]]
            //                    let res = await this.rpc({
            //                        model: 'pos.order',
            //                        method: 'search_read',
            //                        kwargs: {
            //                            domain: domain,
            //                            fields: ['is_printed'],
            //                        },
            //                    });
            //                    //console.log("Res: ", res);
            //                    let is_printed = res ? res[0]['is_printed'] : false;
            //                    //console.log("is_printed: ", is_printed);
            //                    table.billed = is_printed
            //                }
            //                //console.log("Table2: ", table.billed);
            //                return table.billed
            //            }

            get orderBilled() {
                const table = this.props.table;
                return table.billed || false;
            }
    };

    Registries.Component.extend(TableWidget, TableWidgetInherit);

    return TableWidget;
});