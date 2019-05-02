# -*- coding: utf-8 -*-

import datetime
from odoo import models, fields, api, _


class FeeReceipts(models.Model):
    _inherit = 'account.invoice'

    # mofify fields
    student_id = fields.Many2one('education.student', string='Student ID') # Admission No to Student ID

    # add fields
    # TODO remove 'draft' status
    application_id = fields.Many2one('education.application', string='Application No',
                                     domain="[('state', 'in', ['draft', 'verification', 'fee'])]")