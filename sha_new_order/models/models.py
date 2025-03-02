# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class sha_new_order(models.Model):
#     _name = 'sha_new_order.sha_new_order'
#     _description = 'sha_new_order.sha_new_order'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
