from odoo import fields, models, api
from odoo.exceptions import ValidationError

class TupEducationStudentSignup(models.Model):
    _name = 'education.student_signup'
    _description = 'TUP Student Signup'

    #add field
    name = fields.Char(string='Name', required=True, help="Enter Name of Student")
    email = fields.Char(string='Email', required=True, help="Enter Email of Student")
    nrc_no = fields.Char(string='NRC Number', required=True, help="Enter NRC Number of Student")
    password = fields.Char(string='Password', required=True, help="Enter Password of Student")
    confirm_password = fields.Char(string='Confirm Password', required=True, help="Enter Confirm Password of Student")
    #nrc_no = fields.One2one('education.admission', string="NRC Number", required=True,
                             help="Choose Your NRC Number")