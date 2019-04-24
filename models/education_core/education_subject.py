# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class EducationSubject(models.Model):
    _inherit = 'education.subject'
    
    major_id = fields.Many2one('hr.department', string="Major",
                            required=True, domain=[('is_major', '=', True)],
                            help="Choose Major")
    is_tutorial = fields.Boolean(string='Tutorial', help="Tick if this is the Tutorial")
    is_class_work = fields.Boolean(string="Class Work", help="Tick if this is the class Work")