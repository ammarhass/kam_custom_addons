from odoo import models, fields, api

class VendorWizard(models.TransientModel):

    _name = 'vendor.analytic.wizard'

    vendor_id = fields.Many2one('res.partner')


    def vendor_fun(self):
        vendor_id = self.vendor_id.id  # Get the selected account_id from the wizard
        return {
            'type': 'ir.actions.act_url',
            'url': f'/analytic/excel/report/vendor/details/{self.env.context.get("active_ids")}',
            'target': 'new'
        }
