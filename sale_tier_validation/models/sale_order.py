# Copyright 2019 Open Source Integrators
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, api, fields


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = ["sale.order", "tier.validation"]
    _state_from = ["draft", "sent"]
    _state_to = ["sale"]

    _tier_validation_manual_config = False

    @api.model_create_multi
    def create(self, vals_list):
        sales = super().create(vals_list)
        for sale in sales:
            sale.request_validation()
        return sales

    def action_confirm(self):
        res = super().action_confirm()
        return res

    def _get_requested_notification_subtype(self):
        return "sale_tier_validation.sale_order_tier_validation_requested"

    def _get_accepted_notification_subtype(self):
        return "sale_tier_validation.sale_order_tier_validation_accepted"

    def _get_rejected_notification_subtype(self):
        return "sale_tier_validation.sale_order_tier_validation_rejected"
