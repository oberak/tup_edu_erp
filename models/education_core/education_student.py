from odoo import fields, models, _, api
from odoo.exceptions import ValidationError

class EducationStudent(models.Model):
    _name = 'education.student'
    _inherit = 'education.student'
    _description = 'Student Form'

    #modify fields

    medium = fields.Many2one('education.medium', string="Medium", required=False)
    sec_lang = fields.Many2one('education.subject', string="Second language", required=False, domain=[('is_language', '=', True)])
    mother_tongue = fields.Many2one('education.mother.tongue', string="Mother Tongue", required=False, domain=[('is_language', '=', True)])

    #parent's Info
    f_nrc = fields.Char(string='Father NRC Number')
    m_nrc = fields.Char(string='Mother NRC Number',  help="Enter Mother NRC Number")
    f_nationality = fields.Many2one('res.country', string='Father Nationality', ondelete='restrict',
                                  help="Select the Father Nationality")
    m_nationality = fields.Many2one('res.country', string='Mother Nationality', ondelete='restrict',
                                  help="Select the Mother Nationality")
    f_occupation = fields.Char(string='Father Occupation',  help="Enter Father Occupation ")
    m_occupation = fields.Char(string='Mother Occupation', help="Enter Mother Occupation")
    f_religion = fields.Many2one('religion.religion', string="Father Religion", help="My Father Religion is ")
    m_religion = fields.Many2one('religion.religion', string="Mother Religion", help="My Mother Religion is ") 
    sibling_ids = fields.One2many('education.student.sibling', 'student_id', string="Student Sibling")


    major_id = fields.Many2one('hr.department', string="Major",
                            required=True, domain=[('is_major', '=', True)],
                            help="Choose Major")
    student_id=fields.Char(string='Student ID.',  help="Enter Student ID of Student")
    ad_no = fields.Char(string="Admission Number", readonly=True)

class EducationStudentSiblings(models.Model):
    _name = 'education.student.sibling'
    #add fields for sibling's info
    name = fields.Char(string='Sibling Name',  help="Enter Sibling Name")
    nrc_no = fields.Char(string='Sibling NRC Number', help="Enter Sibling NRC Number")
    occupation = fields.Char(string='Sibling Occupation',  help="Enter Sibling Occupation ")
    address = fields.Char(string='Address',  help="Enter Sibling Address")
    student_id = fields.Many2one('education.application', string='Student')    
  

    # _sql_constraints = [
    #     ('student_id', 'unique(student_id)', "Another Student already exists with this student_id number!"),
    # ]
   