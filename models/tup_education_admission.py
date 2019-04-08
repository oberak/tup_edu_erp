# -*- coding: utf-8 -*-

from odoo import fields, models, _, api
from odoo.exceptions import ValidationError

class TupStudentAdmission(models.Model):
    _name = 'education.admission'
    _description = 'Admission for the TUP students'

    #new fields
    name = fields.Char(string='Name', required=True, help="Enter Name of Student")
    roll_no = fields.Char(string='Roll Number', required=True, help="Enter Roll Number of Student")
    nrc_no = fields.Char(string='NRC Number', required=True, help="Enter NRC Number of Student")
    total_mark = fields.Char(string='Total Mark', required=True, help="Enter Total Mark of Student")
    academic_year = fields.Char(string='Academic Year', required=True, help="Enter Academic Year")
    
    