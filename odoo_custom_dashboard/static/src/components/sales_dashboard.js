/** @odoo-module */

import { registry } from "@web/core/registry"
import { KpiCard } from "./kpi_card/kpi_card"
import { ChartRenderer } from "./chart_renderer/chart_renderer"
import { loadJS } from "@web/core/assets"
import { useService } from "@web/core/utils/hooks"
const { Component, onWillStart, useRef, onMounted, useState } = owl
import { getColor } from "@web/views/graph/colors"
import { browser } from "@web/core/browser/browser"
import { routeToUrl } from "@web/core/browser/router_service"

export class OwlSalesDashboard extends Component {
    // top products
    async getTopProducts(){
        let domain = [['state', 'in', ['sale', 'done']]]
        if (this.state.period > 0){
            domain.push(['date','>', this.state.current_date])
        }

        const data = await this.orm.readGroup("sale.report", domain, ['product_id', 'price_total'], ['product_id'], { limit: 5, orderby: "price_total desc" })

        this.state.topProducts = {
            data: {
                labels: data.map(d => d.product_id[1]),
                  datasets: [
                  {
                    label: 'Total',
                    data: data.map(d => d.price_total),
                    hoverOffset: 4,
                    backgroundColor: data.map((_, index) => getColor(index)),
                  },{
                    label: 'Count',
                    data: data.map(d => d.product_id_count),
                    hoverOffset: 4,
                    backgroundColor: data.map((_, index) => getColor(index)),
                }]
            },
            domain,
            label_field: 'product_id',
        }
    }

    // top sales people
    async getTopSalesPeople(){
        let domain = [['state', 'in', ['sale', 'done']]]
        if (this.state.period > 0){
            domain.push(['date','>', this.state.current_date])
        }

        const data = await this.orm.readGroup("sale.report", domain, ['user_id', 'price_total'], ['user_id'], { limit: 5, orderby: "price_total desc" })

        this.state.topSalesPeople = {
            data: {
                labels: data.map(d => d.user_id[1]),
                  datasets: [
                  {
                    label: 'Total',
                    data: data.map(d => d.price_total),
                    hoverOffset: 4,
                    backgroundColor: data.map((_, index) => getColor(index)),
                  }]
            },
            domain,
            label_field: 'user_id',
        }
    }

    // monthly sales
    async getMonthlySales(){
        let domain = [['state', 'in', ['draft','sent','sale', 'done']]]
        if (this.state.period > 0){
            domain.push(['date','>', this.state.current_date])
        }

        const data = await this.orm.readGroup("sale.report", domain, ['date', 'state', 'price_total'], ['date', 'state'], { orderby: "date", lazy: false })
        console.log("monthly sales", data)

        const labels = [... new Set(data.map(d => d.date))]
        const quotations = data.filter(d => d.state == 'draft' || d.state == 'sent')
        const orders = data.filter(d => ['sale','done'].includes(d.state))

        this.state.monthlySales = {
            data: {
                labels: labels,
                  datasets: [
                  {
                    label: 'Quotations',
                    data: labels.map(l=>quotations.filter(q=>l==q.date).map(j=>j.price_total).reduce((a,c)=>a+c,0)),
                    hoverOffset: 4,
                    backgroundColor: "red",
                  },{
                    label: 'Orders',
                    data: labels.map(l=>orders.filter(q=>l==q.date).map(j=>j.price_total).reduce((a,c)=>a+c,0)),
                    hoverOffset: 4,
                    backgroundColor: "green",
                }]
            },
            domain,
            label_field: 'date',
        }
    }

    // partner orders
    async getPartnerOrders(){
        let domain = [['state', 'in', ['draft','sent','sale', 'done']]]
        if (this.state.period > 0){
            domain.push(['date','>', this.state.current_date])
        }

        const data = await this.orm.readGroup("sale.report", domain, ['partner_id', 'price_total', 'product_uom_qty'], ['partner_id'], { orderby: "partner_id", lazy: false })
        console.log(data)

        this.state.partnerOrders = {
            data: {
                labels: data.map(d => d.partner_id[1]),
                  datasets: [
                  {
                    label: 'Total Amount',
                    data: data.map(d => d.price_total),
                    hoverOffset: 4,
                    backgroundColor: "orange",
                    yAxisID: 'Total',
                    order: 1,
                  },{
                    label: 'Ordered Qty',
                    data: data.map(d => d.product_uom_qty),
                    hoverOffset: 4,
                    //backgroundColor: "blue",
                    type:"line",
                    borderColor: "blue",
                    yAxisID: 'Qty',
                    order: 0,
                }]
            },
            scales: {
                /*Qty: {
                    position: 'right',
                }*/
                yAxes: [
                    { id: 'Qty', position: 'right' },
                    { id: 'Total', position: 'left' },
                ]
            },
            domain,
            label_field: 'partner_id',
        }
    }

    setup(){
        this.state = useState({
          customers: [],   // ✅ Initialize customers to an empty array
        partner_id: "",
            quotations: {
                value:10,
                percentage:6,
            },
            custom_revenue:0,
            period:90,
            totalInvestment: {
            value: 0,
            percentage: 0,
        },
        netProfit: {
            value: 0,
            percentage: 0,
        },
        allCompanyInvestments: {
            value: 0,
            percentage: 0,
        },
         allPartnerEquity: {
            value: 0,
            percentage: 0,
        },
         dashboardAccounts: []
        })
        this.orm = useService("orm")
        this.actionService = useService("action")

        const old_chartjs = document.querySelector('script[src="/web/static/lib/Chart/Chart.js"]')
        const router = useService("router")

        if (old_chartjs){
            let { search, hash } = router.current
            search.old_chartjs = old_chartjs != null ? "0":"1"
            hash.action = 86
            browser.location.href = browser.location.origin + routeToUrl(router.current)
        }

        onWillStart(async ()=>{
            this.getDates()
            await this.getQuotations()
            await this.loadCustomers()
            await this.getOrders()

            await this.getTopProducts()
            await this.getTopSalesPeople()
            await this.getMonthlySales()
            await this.getPartnerOrders()
             await this.getTotalInvestment();
        await this.getNetProfit();
        await this.getAllCompanyInvestments();
        await this.getPartnerEquity();

        })
    }
async loadCustomers() {
    const customers = await this.orm.searchRead("res.partner", [['customer_rank', '>', 0]], ["id", "name"]);

    // Ensure no duplicate or undefined keys
    const uniqueCustomers = customers.filter((customer, index, self) =>
        customer.id && self.findIndex(c => c.id === customer.id) === index
    );

    console.log(uniqueCustomers);  // Check the output in the console
    this.state.customers = uniqueCustomers || [];
}
async onChangeCustomer(ev) {
    const selectedCustomerId = parseInt(ev.target.value) || 0;
    console.log("Selected customer ID:", selectedCustomerId);

    // Store the selected customer ID in a separate state variable
    this.state.selectedCustomerId = selectedCustomerId;

    // Do something with the selectedCustomerId
}



    async onChangePeriod(){
        this.getDates()
        await this.getQuotations()
        await this.getOrders()

        await this.getTopProducts()
        await this.getTopSalesPeople()
        await this.getMonthlySales()
        await this.getPartnerOrders()
        await this.getTotalInvestment();
        await this.getNetProfit();
        await this.getAllCompanyInvestments();
    }


    getDates(){
        this.state.current_date = moment().subtract(this.state.period, 'days').format('L')
        this.state.previous_date = moment().subtract(this.state.period * 2, 'days').format('L')
    }

    async getQuotations(){
        let domain = [['state', 'in', ['sent', 'draft']]]
        if (this.state.period > 0){
            domain.push(['date_order','>', this.state.current_date])
        }
        const data = await this.orm.searchCount("sale.order", domain)
        this.state.quotations.value = data

        // previous period
        let prev_domain = [['state', 'in', ['sent', 'draft']]]
        if (this.state.period > 0){
            prev_domain.push(['date_order','>', this.state.previous_date], ['date_order','<=', this.state.current_date])
        }
        const prev_data = await this.orm.searchCount("sale.order", prev_domain)
        const percentage = ((data - prev_data)/prev_data) * 100
        this.state.quotations.percentage = percentage.toFixed(2)
    }
//    async onChangeCustomer() {
//    if (!this.state.partner_id) return;
//
//    let domain = [['state', 'in', ['sale', 'done']], ['partner_id', '=', this.state.partner_id]];
//    let move_domain = [['state', 'in', ['posted']], ['move_type', 'in', ['out_invoice']], ['partner_id', '=', this.state.partner_id]];
//
//    const orders = await this.orm.searchCount("sale.order", domain);
//
//    const move_current_revenue = await this.orm.readGroup("account.move", move_domain, ["amount_total_signed:sum"], []);
//    const prev_revenue = await this.orm.readGroup("account.move", move_domain, ["amount_total_signed:sum"], []);
//
//    const revenue = move_current_revenue[0]?.amount_total_signed || 0;
//    const prev_revenue_value = prev_revenue[0]?.amount_total_signed || 1;  // Prevent division by zero
//    const revenue_percentage = ((revenue - prev_revenue_value) / prev_revenue_value) * 100;
//
//    this.state.orders = {
//        ...this.state.orders,
//        revenue: `$${(revenue / 1000).toFixed(2)}K`,
//        revenue_percentage: revenue_percentage.toFixed(2),
//    };
//}
//
//onChangeCustomRevenue(event) {
//    let newRevenue = parseFloat(event.target.value) || 0;
//    this.state.orders.revenue = `$${(newRevenue / 1000).toFixed(2)}K`;
//
//    let prevRevenue = parseFloat(this.state.orders.revenue.replace("$", "").replace("K", "")) * 1000 || 1;
//    this.state.orders.revenue_percentage = (((newRevenue - prevRevenue) / prevRevenue) * 100).toFixed(2);
//}


    async getOrders(){
        let domain = [['state', 'in', ['sale', 'done']]]
        let move_domain = [['state', 'in', ['posted']],
              ['move_type', 'in', ['out_invoice']]];
        if (this.state.period > 0){
            domain.push(['date_order','>', this.state.current_date])
        }
        const data = await this.orm.searchCount("sale.order", domain)
        //this.state.quotations.value = data

        // previous period
        let prev_domain = [['state', 'in', ['sale', 'done']]]
        if (this.state.period > 0){
            prev_domain.push(['date_order','>', this.state.previous_date], ['date_order','<=', this.state.current_date])
        }
        const prev_data = await this.orm.searchCount("sale.order", prev_domain)
        const percentage = ((data - prev_data)/prev_data) * 100
        //this.state.quotations.percentage = percentage.toFixed(2)

        //revenues
        const move_current_revenue = await this.orm.readGroup("account.move", move_domain, ["amount_total_signed:sum"], [])
        const current_revenue = await this.orm.readGroup("account.move", move_domain, ["amount_total_signed:sum"], [])
        const prev_revenue = await this.orm.readGroup("account.move", move_domain, ["amount_total_signed:sum"], [])
        const revenue_percentage = ((current_revenue[0].amount_total_signed - prev_revenue[0].amount_total_signed) / prev_revenue[0].amount_total_signed) * 100

        //average
        const current_average = await this.orm.readGroup("sale.order", domain, ["amount_total:avg"], [])
        const prev_average = await this.orm.readGroup("sale.order", prev_domain, ["amount_total:avg"], [])
        const average_percentage = ((current_average[0].amount_total - prev_average[0].amount_total) / prev_average[0].amount_total) * 100

        this.state.orders = {
            value: data,
            percentage: percentage.toFixed(2),
            revenue: `$${(move_current_revenue[0].amount_total_signed/1000).toFixed(2)}K`,
            revenue_percentage: revenue_percentage.toFixed(2),
            average: `$${(current_average[0].amount_total_signed/1000).toFixed(2)}K`,
            average_percentage: average_percentage.toFixed(2),
        }

        //this.env.services.company
    }

    async viewQuotations(){
        let domain = [['state', 'in', ['sent', 'draft']]]
        if (this.state.period > 0){
            domain.push(['date_order','>', this.state.current_date])
        }

        let list_view = await this.orm.searchRead("ir.model.data", [['name', '=', 'view_quotation_tree_with_onboarding']], ['res_id'])

        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Quotations",
            res_model: "sale.order",
            domain,
            views: [
                [list_view.length > 0 ? list_view[0].res_id : false, "list"],
                [false, "form"],
            ]
        })
    }

    viewOrders(){
        let domain = [['state', 'in', ['sale', 'done']]]
        if (this.state.period > 0){
            domain.push(['date_order','>', this.state.current_date])
        }

        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Quotations",
            res_model: "sale.order",
            domain,
            context: {group_by: ['date_order']},
            views: [
                [false, "list"],
                [false, "form"],
            ]
        })
    }
    async viewTotalInvestment() {
    let domain = [['account_type', 'in', ['equity', 'equity_unaffected']]];

    this.actionService.doAction({
        type: "ir.actions.act_window",
        name: "Total Investment",
        res_model: "account.account",
        domain,
        views: [
            [false, "list"],
            [false, "form"],
        ]
    });
}

async viewNetProfit() {

    let domain = [['account_type', 'in', ['income', 'income_other', 'expense_direct_cost','expense']]];
    this.actionService.doAction({
        type: "ir.actions.act_window",
        name: "Net Profit",
        res_model: "account.account",
        domain,
        views: [
            [false, "list"],
            [false, "form"],
        ]
    });
}
 async onChangeCustomRevenue(ev) {
    this.state.custom_revenue = parseFloat(ev.target.value) || 0;
    this.getTotalInvestment();  // Recalculate when value changes
    this.getNetProfit();  // Recalculate when value changes
    this.getPartnerEquity();  // Recalculate when value changes

}
async getPartnerEquity() {
    let income = await this.orm.readGroup("account.account", [['account_type', '=', 'income']], ['current_balance_Stored:sum'], []);
    let incomeValue = income[0].current_balance_Stored;
    let other_income = await this.orm.readGroup("account.account", [['account_type', '=', 'income_other']], ['current_balance_Stored:sum'], []);
    let other_incomeValue = other_income[0].current_balance_Stored;
    let expenses = await this.orm.readGroup("account.account", [['account_type', '=', 'expense']], ['current_balance_Stored:sum'], []);
    let expensesValue = expenses[0].current_balance_Stored;

    let cost_of_revenue = await this.orm.readGroup("account.account", [['account_type', '=', 'expense_direct_cost']], ['current_balance_Stored:sum'], []);
    let cost_of_revenueValue = cost_of_revenue[0].current_balance_Stored;
    let total_company_investment = await this.orm.readGroup("account.account", [['account_type', 'in', ['equity', 'equity_unaffected']]], ['current_balance_Stored:sum'], []);
    let total_company_investmentValue = total_company_investment[0].current_balance_Stored;
    let totalNetProfitValue = incomeValue + other_incomeValue - cost_of_revenueValue - expensesValue
    // Round the current_balance_Stored to 2 decimal places
    let roundedValue = totalNetProfitValue + total_company_investmentValue;
    if (this.state.custom_revenue > 0) {
        roundedValue *= (this.state.custom_revenue / 100);
    }
    this.state.allPartnerEquity = {
        value:  `$${(roundedValue/1000).toFixed(2)}K`,
        percentage: 0, // You can calculate percentage change if needed

//         value: data,
//            percentage: percentage.toFixed(2),
//            revenue: `$${(current_revenue[0].amount_total/1000).toFixed(2)}K`,
//            revenue_percentage: revenue_percentage.toFixed(2),
//            average: `$${(current_average[0].amount_total/1000).toFixed(2)}K`,
//            average_percentage: average_percentage.toFixed(2),
    };
}
async viewPartnerEquity() {
    let domain = [['account_type', 'in', ['equity', 'equity_unaffected', 'income', 'income_other', 'expense_direct_cost','expense']]];  // Adjust "balance" to the correct field name

    this.actionService.doAction({
        type: "ir.actions.act_window",
        name: "All Company Investments",
        res_model: "account.account",
        domain,
        views: [
            [false, "list"],
            [false, "form"],
        ]
    });
}
async viewAllCompanyInvestments() {
    let domain = [["current_balance_Stored", ">", 0]];  // Adjust "balance" to the correct field name

    this.actionService.doAction({
        type: "ir.actions.act_window",
        name: "All Company Investments",
        res_model: "account.account",
        domain,
        views: [
            [false, "list"],
            [false, "form"],
        ]
    });
}
   async getTotalInvestment() {
    let domain = [['account_type', 'in', ['equity', 'equity_unaffected']]];
    const data = await this.orm.readGroup("account.account", domain, ['current_balance_Stored:sum'], []);
    console.log('datadata', data); // Debugging

    // Round the current_balance_Stored to 2 decimal places
    let roundedValue = Math.round(data[0].current_balance_Stored * 100) / 100;
    if (this.state.custom_revenue > 0) {
        roundedValue *= (this.state.custom_revenue / 100);
    }
//    if (this.state.custom_revenue > 0) {
//        roundedValue *= (this.state.custom_revenue / 100);
//    }



    this.state.totalInvestment = {
        value:  `$${(roundedValue/1000).toFixed(2)}K`,
        percentage: 0, // You can calculate percentage change if needed

//         value: data,
//            percentage: percentage.toFixed(2),
//            revenue: `$${(current_revenue[0].amount_total/1000).toFixed(2)}K`,
//            revenue_percentage: revenue_percentage.toFixed(2),
//            average: `$${(current_average[0].amount_total/1000).toFixed(2)}K`,
//            average_percentage: average_percentage.toFixed(2),
    };
}

// Net Profit
async getNetProfit() {

    // Fetch total investment data
//    [['account_type', 'in', ['income', 'income_other', 'expense_direct_cost','expense']]]
    let income = await this.orm.readGroup("account.account", [['account_type', '=', 'income']], ['current_balance_Stored:sum'], []);
    let incomeValue = income[0].current_balance_Stored;
    let other_income = await this.orm.readGroup("account.account", [['account_type', '=', 'income_other']], ['current_balance_Stored:sum'], []);
    let other_incomeValue = other_income[0].current_balance_Stored;
    let expenses = await this.orm.readGroup("account.account", [['account_type', '=', 'expense']], ['current_balance_Stored:sum'], []);
    let expensesValue = expenses[0].current_balance_Stored;

    let cost_of_revenue = await this.orm.readGroup("account.account", [['account_type', '=', 'expense_direct_cost']], ['current_balance_Stored:sum'], []);
    let cost_of_revenueValue = cost_of_revenue[0].current_balance_Stored;
    let totalInvestmentDomain = [['is_dashboard', '=', true]];
//    let domain = [['is_dashboard', '=', true]];
        const accountsData = await this.orm.searchRead("account.account", totalInvestmentDomain, ['name', 'current_balance_Stored']);
        this.state.dashboardAccounts = accountsData.map(account => ({
        name: account.name,
        balance: account.current_balance_Stored || 0
    }));
    console.log(this.state.dashboardAccounts);


//    let totalInvestmentData = await this.orm.readGroup("account.account", totalInvestmentDomain, ['current_balance_Stored:sum'], []);
    let totalInvestmentValue = incomeValue + other_incomeValue - cost_of_revenueValue - expensesValue

    // Fetch all company investments data
    let allCompanyInvestmentsDomain = [["current_balance_Stored", ">", 0]];
    const allCompanyInvestmentsData = await this.orm.readGroup("account.account", allCompanyInvestmentsDomain, ['current_balance_Stored:sum'], []);
    const allCompanyInvestmentsValue = allCompanyInvestmentsData[0].current_balance_Stored;
    if (this.state.custom_revenue > 0) {
        totalInvestmentValue *= (this.state.custom_revenue / 100);
    }

    // Calculate the net profit percentage
    const netProfitPercentage = (totalInvestmentValue / allCompanyInvestmentsValue) * 100;

    // Update the state with the new net profit value and percentage
    this.state.netProfit = {

        value: `$${(totalInvestmentValue/1000).toFixed(2)}K`,
        percentage: 0, // Round to 2 decimal places
    };
}

// All Company Investments
async getAllCompanyInvestments() {
    let domain = [["current_balance_Stored", ">", 0]];
    const data = await this.orm.readGroup("account.account", domain, ['current_balance_Stored:sum'], []);

    // Round the totalBalance to 2 decimal places
//    const roundedTotalBalance = Math.round(totalBalance * 100) / 100;

    this.state.allCompanyInvestments = {

        value: `$${((Math.round(data[0].current_balance_Stored * 100) / 100)/1000).toFixed(2)}K`,
        percentage: 0, // You can calculate percentage change if needed
    };
}

    viewRevenues(){
        let domain = [['state', 'in', ['posted']],
              ['move_type', 'in', ['out_invoice']]];

//        if (this.state.period > 0){
//            domain.push(['date_order','>', this.state.current_date])
//        }

        this.actionService.doAction({
            type: "ir.actions.act_window",
            name: "Invoices",
            res_model: "account.move",
            domain,
            context: {group_by: ['invoice_date']},
            views: [
                [false, "list"],
            [false, "form"],
            ]
        })
    }
}

OwlSalesDashboard.template = "owl.OwlSalesDashboard"
OwlSalesDashboard.components = { KpiCard, ChartRenderer }

registry.category("actions").add("owl.sales_dashboard", OwlSalesDashboard)