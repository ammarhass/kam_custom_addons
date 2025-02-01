from odoo import models, fields, api


class InheritProductTemplate(models.Model):
    _inherit = 'product.template'


    def wiz_open(self):
        print("action" ,self.env['ir.actions.act_window']._for_xml_id("product_custom.fields_average_wizard_actions"))
        return self.env['ir.actions.act_window']._for_xml_id("product_custom.fields_average_wizard_actions")
