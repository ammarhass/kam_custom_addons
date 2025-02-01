from odoo import models, fields, api


class InheritResPartner(models.Model):
    _inherit = 'res.partner'

    default_sequence = fields.Char()

    @api.model_create_multi
    def create(self, vals_list):
        partners = super().create(vals_list)
        for part in partners:
            print("hello")
            self._update_reference_number(part)
        return partners

    def _update_reference_number(self, partner):
        # search_partner_mode = self.env.context.get('res_partner_search_mode')
        if partner.supplier_rank:
            prefix = 'Ven_'
            all_words = prefix + str(
                len((self.env['res.partner'].search([]).filtered(lambda x: x.supplier_rank != 0 and x.customer_rank == 0))))
            string_without_spaces = all_words.replace(" ", "")
            partner.default_sequence = string_without_spaces
        elif partner.customer_rank:
            prefix = 'Cust_'
            all_words = prefix + str(
                len((self.env['res.partner'].search([]).filtered(lambda x: x.customer_rank != 0 and x.supplier_rank == 0))))
            string_without_spaces = all_words.replace(" ", "")
            partner.default_sequence = string_without_spaces

        return True

    # def write(self, vals):
    #     print('hello from write')
    #     if 'supplier_rank' or 'customer_rank' in vals:
    #         print('vals')
    #         self._update_reference_number(vals)
    #     return super().write(vals)


    def update_product_sequence(self):

        partners = self.env['res.partner'].search(domain=[], order='id')
        ven_sequence_number = 1
        cus_sequence_number = 1
        cus_ven_sequence_number = 1
        for partner in partners:
            if partner.supplier_rank and partner.customer_rank:
                prefix = 'Cust/Ven_'
                all_words = prefix + str(cus_ven_sequence_number)
                default_sequence = all_words.replace(" ", "")
                partner.write(
                    {
                        "default_sequence": default_sequence,
                    }
                )
                cus_ven_sequence_number = cus_ven_sequence_number + 1
            elif partner.supplier_rank:
                prefix = 'Ven_'
                all_words = prefix + str(ven_sequence_number)
                default_sequence = all_words.replace(" ", "")
                partner.write(
                    {
                        "default_sequence": default_sequence,
                    }
                )
                ven_sequence_number = ven_sequence_number + 1
            elif partner.customer_rank:
                prefix = 'Cust_'
                all_words = prefix + str(cus_sequence_number)
                default_sequence = all_words.replace(" ", "")
                partner.write(
                    {
                        "default_sequence": default_sequence,
                    }
                )
                cus_sequence_number = cus_sequence_number + 1