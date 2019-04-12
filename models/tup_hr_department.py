# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class HrDepartment(models.Model):
    _inherit = 'hr.department'

    is_major = fields.Boolean(string="is Major", help="Tick if this department is a Major")
    can_enroll = fields.Boolean(string="Enrollment possible", help="Tick if this department can enroll")
    major_code =fields.Char('Major code', help="Major code")

    _sql_constraints = [ ('major_code', 'unique (major_code)','Major code already exists for another Major!') ]
