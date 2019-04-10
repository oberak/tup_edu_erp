# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class EducationSubject(models.Model):
    _inherit = 'education.subject'
    major_id = fields.Many2one('hr.department', string="Major",
                            required=True, domain=[('is_major', '=', True)],
                            help="Choose Major")