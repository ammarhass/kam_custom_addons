from odoo import models, fields, api


class InheritPurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def wiz_open(self):
        print("action" ,self.env['ir.actions.act_window']._for_xml_id("product_custom.fields_average_wizard_actions"))
        return self.env['ir.actions.act_window']._for_xml_id("product_custom.fields_average_wizard_actions")

    def wiz_open2(self):
        print("action" ,self.env['ir.actions.act_window']._for_xml_id("product_custom.create_unbuild_order_action"))
        return self.env['ir.actions.act_window']._for_xml_id("product_custom.create_unbuild_order_action")

    def _add_supplier_to_product(self):
        # Add the partner in the supplier list of the product if the supplier is not registered for
        # this product. We limit to 10 the number of suppliers for a product to avoid the mess that
        # could be caused for some generic products ("Miscellaneous").
        if self.env.company.elazz_comp:
            for line in self.order_line:
                # Do not add a contact as a supplier
                partner = self.partner_id if not self.partner_id.parent_id else self.partner_id.parent_id
                already_seller = (partner | self.partner_id) & line.product_id.seller_ids.mapped('partner_id')
                if line.product_id:
                    # Convert the price in the right currency.
                    currency = partner.property_purchase_currency_id or self.env.company.currency_id
                    price = self.currency_id._convert(line.price_unit, currency, line.company_id, line.date_order or fields.Date.today(), round=False)
                    # Compute the price for the template's UoM, because the supplier's UoM is related to that UoM.
                    if line.product_id.product_tmpl_id.uom_po_id != line.product_uom:
                        default_uom = line.product_id.product_tmpl_id.uom_po_id
                        price = line.product_uom._compute_price(price, default_uom)
    
                    supplierinfo = self._prepare_supplier_info(partner, line, price, currency)
                    # In case the order partner is a contact address, a new supplierinfo is created on
                    # the parent company. In this case, we keep the product name and code.
                    seller = line.product_id._select_seller(
                        partner_id=line.partner_id,
                        quantity=line.product_qty,
                        date=line.order_id.date_order and line.order_id.date_order.date(),
                        uom_id=line.product_uom)
                    if seller:
                        supplierinfo['product_name'] = seller.product_name
                        supplierinfo['product_code'] = seller.product_code
                    vals = {
                        'seller_ids': [(0, 0, supplierinfo)],
                    }
                    # supplier info should be added regardless of the user access rights
                    line.product_id.product_tmpl_id.sudo().write(vals)
        return super()._add_supplier_to_product()



    def _prepare_supplier_info(self, partner, line, price, currency):
        # Prepare supplierinfo data when adding a product
        if self.env.company.elazz_comp:
            return {
                'partner_id': partner.id,
                'sequence': max(line.product_id.seller_ids.mapped('sequence')) + 1 if line.product_id.seller_ids else 1,
                'min_qty': line.product_qty,
                'price': line.price_subtotal,
                'currency_id': currency.id,
                'delay': 0,
                'net_value': line.net_value,
                'fraction_value': line.fraction_value,
                'white_rice_quantity': line.white_rice_quantity,
                'fraction_quantity': line.fraction_quantity,
                'good_rice_quantity': line.good_rice_quantity,
                'date': line.create_date.date()
            }
        return super()._prepare_supplier_info(partner, line, price, currency)
