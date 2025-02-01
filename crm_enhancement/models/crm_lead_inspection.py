from odoo import models, api, fields
from odoo.exceptions import ValidationError
class CRMLeadInspection(models.Model):
    _name = 'crm.lead.inspection'
    _description = 'جدول فحص الفرص'

    lead_id = fields.Many2one('crm.lead', string="الفرصة")
    item_number = fields.Integer(readonly=True, string="م")
    recommendation = fields.Text(string="التوصية")
    old_or_damaged_part = fields.Char(string="القطعة القديمة أو التالفة")
    new_or_repaired_part = fields.Char(string="القطعة الجديدة أو الإصلاح")
    work_done = fields.Char(string="ما تم عمله")
    cost = fields.Float(string="التكلفة")
    repair_location = fields.Char(string="مكان الإصلاح")
    invoice = fields.Char(string="الفاتورة")
    location = fields.Char(string="لوكيشن")
    telephone = fields.Char(string="Tel")
    remarks = fields.Text(string="ملاحظات")

    @api.model
    def create(self, vals):
        # Find the max item_number from existing crm.lead.inspection records
        max_item_number = self.search([], limit=1, order="item_number desc")
        # Set item_number to the next available number (max_item_number + 1)
        if max_item_number:
            vals['item_number'] = max_item_number.item_number + 1
        else:
            vals['item_number'] = 1  # Start with 1 if there are no records
        return super(CRMLeadInspection, self).create(vals)

    def write(self, vals):
        # Ensure item_number is updated based on the existing records for the same lead_id
        if 'lead_id' in vals:
            # If lead_id is changed, reset the item_number for the new lead
            lead_id = vals.get('lead_id', self.lead_id.id)
        else:
            lead_id = self.lead_id.id

        # Get all inspections for the same lead_id sorted by the current item_number (if any)
        inspections = self.search([('lead_id', '=', lead_id)], order="item_number asc")

        # Re-assign item_numbers to all inspections under this lead
        for index, inspection in enumerate(inspections, start=1):
            inspection.write({'item_number': index})

        return super(CRMLeadInspection, self).write(vals)