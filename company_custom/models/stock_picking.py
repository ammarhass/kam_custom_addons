from odoo import models, fields, api
from odoo.exceptions import ValidationError


class InheritStockPicking(models.Model):
    _inherit = 'stock.picking'


    @api.model
    def create(self, vals_list):
        print(vals_list)
        res = super().create(vals_list)
        return res


    def button_validate(self):
        for rec in self:
            if rec.company_id.external_transfer:
                if not rec.message_attachment_count:
                    raise ValidationError("Please add an attachment to the record")
        return super().button_validate()
