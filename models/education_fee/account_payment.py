# -*- coding: utf-8 -*-

import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class account_payment(models.Model):
    _inherit = "account.payment"

    # Override for application fee
    @api.multi
    def post(self):
      res = super(account_payment, self).post()
      # change student application state
      for rec in self:
        if(rec.invoice_ids.application_id):
          if rec.invoice_ids.application_id.student_type == 'is_new_candidate':
            rec.invoice_ids.application_id.write({ 'state': 'fee' })
          else:
            rec.invoice_ids.application_id.write({ 'state': 'major' })
      return res