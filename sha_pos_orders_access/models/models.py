# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class sha_pos_orders_access(models.Model):
#     _name = 'sha_pos_orders_access.sha_pos_orders_access'
#     _description = 'sha_pos_orders_access.sha_pos_orders_access'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
