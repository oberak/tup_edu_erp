# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Tup_EducationTimeTable(models.Model):
    _name = 'education.timetable'
    _inherit = 'education.timetable'
    _description = 'Timetable'
    color = fields.Integer()

   
