# -*- coding: utf-8 -*-

from odoo import fields, models, _, api
from odoo.exceptions import ValidationError

class StudentApplication(models.Model):
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

    class_id = fields.Many2one('education.class.division', string='Class',
                               help="Select the class")
    #add fields for new candidate
    #fiscalyear_last_month = fields.Selection([(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], default=12, required=True)
    student_type=fields.Selection([('is_new_candidate','Is New Candidate'),('transfer_in','Is Transfer In Student')], default='transfer_in',required=True)
    
    first_choice = fields.Many2one('hr.department', string="First Choice",
                            required=True, domain=[('can_enroll', '=', True) and ('is_major', '=', True)],
                            help="Choose Major to apply")
    second_choice = fields.Many2one('hr.department', string="Second Choice",
                            required=True, domain=[('can_enroll', '=', True) and ('is_major', '=', True)],
                            help="Choose Major to apply")
    third_choice = fields.Many2one('hr.department', string="Third Choice",
                            required=True,  domain=[('can_enroll', '=', True) and ('is_major', '=', True)],
                            help="Choose Major to apply")
    forth_choice = fields.Many2one('hr.department', string="Forth Choice",
                           domain=[('can_enroll', '=', True) and ('is_major', '=', True)],
                            help="Choose Major to apply")
    fifth_choice = fields.Many2one('hr.department', string="Fifth Choice",
                            domain=[('can_enroll', '=', True) and ('is_major', '=', True)],
                            help="Choose Major to apply")
    admission_no=fields.Char(string='Admission No.', required=True, help="Enter Admission No. of Student")
    roll_no = fields.Char(string='Roll Number', required=True, help="Enter Matriculation Exam Roll Number of Student")
    total_marks = fields.Char(string='Total Marks', required=True, help="Enter Matriculation Exam Total Marks of Student")
    
    _sql_constraints = [
        ('admission_no', 'unique(admission_no)', "Another Student already exists with this admission number!"),
    ]