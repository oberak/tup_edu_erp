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
    #add fields if student is new candidate
    is_new_candidate = fields.Boolean(string="Is New Candidate", default=False,
                                     help="Tick the field if the student is new candidate")
    first_choice = fields.Selection([('IT', 'Information Technology'), ('EC', 'Electronic'), ('EP', 'Electrical Power'), ('MC', 'Mechatronics Engineering'),
                                ('Civil', 'Civil'), ('Mech', 'Mechnical Engineering')],
                                string='first_choice', required=False, default='', track_visibility='onchange',
                                help="Your First Choice to apply major is ")
    second_choice = fields.Selection([('IT', 'Information Technology'), ('EC', 'Electronic'), ('EP', 'Electrical Power'), ('MC', 'Mechatronics Engineering'),
                                ('Civil', 'Civil'), ('Mech', 'Mechnical Engineering')],
                                string='second_choice', required=False, default='', track_visibility='onchange',
                                help="Your Second Choice to apply major is ")
    third_choice = fields.Selection([('IT', 'Information Technology'), ('EC', 'Electronic'), ('EP', 'Electrical Power'), ('MC', 'Mechatronics Engineering'),
                                ('Civil', 'Civil'), ('Mech', 'Mechnical Engineering')],
                                string='third_choice', required=False, default='', track_visibility='onchange',
                                help="Your Third Choice to apply major is ")
    forth_choice = fields.Selection([('IT', 'Information Technology'), ('EC', 'Electronic'), ('EP', 'Electrical Power'), ('MC', 'Mechatronics Engineering'),
                                ('Civil', 'Civil'), ('Mech', 'Mechnical Engineering')],
                                string='forth_choice', required=False, default='', track_visibility='onchange',
                                help="Your Forth Choice to apply major is ")