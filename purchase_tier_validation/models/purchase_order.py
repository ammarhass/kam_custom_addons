# Copyright 2017 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _name = "purchase.order"
    _inherit = ["purchase.order", "tier.validation"]
    _state_from = ["draft", "sent", "to approve"]
    _state_to = ["purchase", "approved"]

    @api.model_create_multi
    def create(self, vals_list):
        purchases = super().create(vals_list)
        for purchase in purchases:
            purchase.request_validation()
        return purchases

    _tier_validation_manual_config = False
