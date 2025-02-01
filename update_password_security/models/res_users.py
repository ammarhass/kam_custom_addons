import re
from datetime import datetime, timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

class ResUsers(models.Model):
    _inherit = "res.users"

    ignore_password_policy = fields.Boolean("Ignore Password Policy")

    def _check_password(self, password):
        if not self.ignore_password_policy:
            self._check_password_rules(password)
            self._check_password_history(password)
        return True

    def _validate_pass_reset(self):
        """It provides validations before initiating a pass reset email
        :raises: UserError on invalidated pass reset attempt
        :return: True on allowed reset
        """
        for user in self:
            if not user.ignore_password_policy:
                pass_min = user.company_id.password_minimum
                if pass_min <= 0:
                    continue
                write_date = user.password_write_date
                if write_date and write_date + timedelta(hours=pass_min) > datetime.now():
                    raise UserError(
                        _(
                            "Passwords can only be reset every %d hour(s). "
                            "Please contact an administrator for assistance."
                        )
                        % pass_min
                    )
        return True

