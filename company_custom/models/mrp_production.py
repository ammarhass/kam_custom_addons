from odoo import models, fields, api
from odoo.exceptions import ValidationError


class InheritMrpProduction(models.Model):
    _inherit = 'mrp.production'

    def button_mark_done(self):
        for rec in self:
            if rec.company_id.manufacturing_order:
                if not rec.message_attachment_count:
                    raise ValidationError("Please add an attachment to the record")
            return super().button_mark_done()