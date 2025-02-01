from odoo import models, fields, api

class ProductTemplate(models.Model):

    _inherit = 'product.template'

    reminder_message = fields.Text()
    reminder_date = fields.Date()
    reminder_user_id = fields.Many2one('res.users')
    fop = fields.Char()
    cpm = fields.Char()

    @api.model
    def send_reminder_message(self):
        recs = self.env['product.template'].search([('reminder_date', '=', fields.Date.today())])
        for rec in recs:
            user_id = rec.reminder_user_id  # Replace with the actual user reference
            message = rec.reminder_message  # Customize your message
            rec.activity_schedule(
                'pearl_sale_order.mail_activity_type_waiting_approval',
                user_id=rec.reminder_user_id.id,
                summary=rec.reminder_message,
            )

        # Create a message
        # recs = self.env['mail.message'].sudo().create({
        #     'body': message,
        #     'message_type': 'notification',
        #     'subtype_id': self.env.ref('mail.mt_comment').id,
        #     'res_id': rec.id,
        #     'model': 'product.template',
        #     'author_id': user_id.partner_id.id,  # The user sending the message
        # })
        # print("rec", recs)
