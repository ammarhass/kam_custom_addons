from odoo import models, fields, api
from odoo.exceptions import ValidationError


class InheritAccountMove(models.Model):
    _inherit = 'account.move'

    def action_post(self):
        for rec in self:
            if rec.move_type == 'out_invoice':
                if rec.company_id.sales_invoice:
                        if not rec.attachment_ids:
                             raise ValidationError("Please add an attachment to the record")
            elif rec.move_type == 'in_invoice':
                if rec.company_id.vendor_bill:
                        if not rec.attachment_ids:
                            raise ValidationError("Please add an attachment to the record")
            elif rec.move_type == 'entry':
                if rec.company_id.journal_entry:
                        if not rec.attachment_ids:
                            raise ValidationError("Please add an attachment to the record")
        return super().action_post()