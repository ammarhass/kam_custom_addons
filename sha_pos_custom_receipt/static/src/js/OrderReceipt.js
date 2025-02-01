odoo.define('sha_pos_custom_receipt.OrderReceipt', function (require) {
    'use strict';

    const OrderReceipt = require('point_of_sale.OrderReceipt')
    const Registries = require('point_of_sale.Registries');

    const OrderReceiptEdit = OrderReceipt =>
        class extends OrderReceipt {

            get receipt() {
//                console.log("this: ", this._receiptEnv.receipt.cashier)
//                console.log("this: ", this)
                let cashierNewName = this.env.pos.cashier['emp_name']
                console.log("cashierNewName: ", cashierNewName)
                //               Order  Name Edit
                let name = this.receiptEnv.receipt.name
                let name1 = name.replace("Order", "")
                let name2 = name1.split(" ")
                this.receiptEnv.receipt.newName = name2[1];
                //                Order Date Edit
                let receipt = this.receiptEnv.receipt
                let day = receipt.date.validation_date.getDate()
                let dayStr = day.toString();
                let month = receipt.date.validation_date.getMonth() + 1;
                let monthStr = month.toString();
                let year = receipt.date.year - 2000
//                console.log("year: ", year);
                let yearStr = year.toString();
//                console.log("yearStr: ", yearStr);
                if (monthStr.length <2){
                    monthStr = "0"+month.toString();
                }
                let hour = receipt.date.validation_date.getHours()
                let minutes = receipt.date.validation_date.getMinutes()
                let newDate = monthStr+dayStr+"-"+yearStr+"-"+hour+minutes
                this.receiptEnv.receipt.newDate = newDate;
                this.receiptEnv.receipt.title = this.env.pos.config.receipt_title || "";
                this.receiptEnv.receipt.cashierNewName = cashierNewName || "";
                return this.receiptEnv.receipt;
            }

        }
    Registries.Component.extend(OrderReceipt, OrderReceiptEdit)
    return OrderReceiptEdit
});
