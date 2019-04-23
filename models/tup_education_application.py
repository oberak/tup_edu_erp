# -*- coding: utf-8 -*-

from odoo import fields, models, _, api
from odoo.exceptions import ValidationError

class TupStudentApplication(models.Model):
    _name = 'education.application'
    _inherit = 'education.application'
    _description = 'Applications for the TUP admission'

    # add fields
    nrc_no = fields.Char(string='NRC Number', required=True, help="Enter NRC Number of Student")

    # modify fields
    medium = fields.Many2one('education.medium', string="Medium", required=False,
                             help="Choose the Medium of class, like English, Hindi etc") # remove required
    sec_lang = fields.Many2one('education.subject', string="Second language",
                            required=False, domain=[('is_language', '=', True)],
                            help="Choose the Second language") # remove required
    admission_class = fields.Many2one('education.class', string="Class", required=False,
                                        help="Enter Class to which the admission is seeking") # remove required
    mother_tongue = fields.Many2one('education.mother.tongue', string="Mother Tongue",
                                    required=False, help="Enter Student's Mother Tongue") # remove required
    nationality = fields.Many2one('res.country', string='Nationality', ondelete='restrict',
                                  help="Select the Nationality", default=145) # set default as Myanmar
    guardian_name = fields.Many2one('res.partner', string="Guardian", domain=[('is_parent', '=', True)], required=False,
                                    help="Tell us who will take care of you") # remove required
    blood_group = fields.Selection([('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('o+', 'O+'), ('o-', 'O-'),
                                ('ab-', 'AB-'), ('ab+', 'AB+')],
                                string='Blood Group', required=False, default='', track_visibility='onchange',
                                help="Your Blood Group is ")
    #add fields for new candidate
    is_new_candidate = fields.Boolean(string="Is New Candidate", default=False,
                                     help="Tick the field if the student is new candidate")
    first_choice = fields.Many2one('hr.department', string="First Choice",
                            required=True, domain=[('can_enroll', '=', True) and ('is_major', '=', True)],
                            help="Choose Major")
    second_choice = fields.Many2one('hr.department', string="Second Choice",
                            required=True, domain=[('can_enroll', '=', True) and ('is_major', '=', True)],
                            help="Choose Major")
    third_choice = fields.Many2one('hr.department', string="Third Choice",
                            required=True,  domain=[('can_enroll', '=', True) and ('is_major', '=', True)],
                            help="Choose Major")
    forth_choice = fields.Many2one('hr.department', string="Forth Choice",
                           domain=[('can_enroll', '=', True) and ('is_major', '=', True)],
                            help="Choose Major")
    fifth_choice = fields.Many2one('hr.department', string="Fifth Choice",
                            domain=[('can_enroll', '=', True) and ('is_major', '=', True)],
                            help="Choose Major")
    admission_no=fields.Char(string='Admission No.', required=True, help="Enter Admission No. of Student", readonly=True)
    roll_no = fields.Char(string='Roll Number', required=True, help="Enter Matriculation Exam Roll Number of Student",readonly=True)
    total_marks = fields.Char(string='Total Marks', required=True, help="Enter Matriculation Exam Total Marks of Student",readonly=True)
    
    _sql_constraints = [
        ('admission_no', 'unique(admission_no)', "Another Student already exists with this admission number!"),
    ]