# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class EducationTimeTable(models.Model):
    _name = 'education.timetable'
    _inherit = 'education.timetable'
    _description = 'Timetable'
    color = fields.Integer()

class EducationTimeTableSchedule(models.Model):
    _inherit = 'education.timetable.schedule'

    subject = fields.Many2one('education.subject', string='Subjects', required=False)
    faculty_id = fields.Many2one('education.faculty', string='Faculty', required=False)