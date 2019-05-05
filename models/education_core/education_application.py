# -*- coding: utf-8 -*-

from odoo import fields, models, _, api
from odoo.exceptions import ValidationError

class StudentApplication(models.Model):
    _name = 'education.application'
    _inherit = 'education.application'
    _order = 'total_marks desc'
    #_inherits = {'res.partner': 'partner_id'}
    _description = 'Applications for the TUP admission'

    #change status depends on transfer_in student
    @api.onchange('student_type','state')
    def on_change_status(self):
        for rec in self:
            if rec.student_type == 'transfer_in':
                rec.state= 'apply'
                # print(rec.state)
            return

   
    #This function is triggered when the user clicks on the button 'Apply Major'
    @api.one
    def apply_major(self, vals):
        for rec in self:
            values = {
                    'first_choice': rec.first_choice,
                    'second_choice': rec.second_choice,
                    'third_choice': rec.third_choice,
                    'forth_choice': rec.forth_choice,
                    'fifth_choice': rec.fifth_choice,
                    }
            self.env['education.application'].update(values)
            
            rec.write({
                'state': 'apply'
                })
        return
        
    #This function is triggered when the user clicks on the button 'Payment for Tution Fee'
    @api.one
    def paid_fee(self):
        for rec in self:
            rec.write({
                'state': 'fee'
            })

    @api.one
    def assign_major(self):
        for rec in self:
            rec.write({
                'state': 'major'
            })

    #change status depends on transfer_in student
    @api.onchange('student_id')
    def student_id(self):
        for rec in self:
            print(len(rec.student_id))

    
    # add fields
    nrc_no = fields.Char(string='NRC Number', required=True, help="Enter NRC Number of Student")

    # modify fields
    academic_year_id = fields.Many2one('education.academic.year', string='Academic Year', required=True, 
                            default=lambda self: self.env['education.academic.year']._get_current_ay(),
                            help="Select the Academic Year")
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
    
    #modify status 
    state = fields.Selection([('draft', 'Draft'), ('apply', 'Apply'),('verification', 'Verify'),('fee', 'Tution Fee'),('major', 'Assign Major'),
                              ('approve', 'Approve'), ('reject', 'Reject'), ('done', 'Done')],
                             string='State', default='draft', track_visibility='onchange')
    
    #add fields for payment
    #payment_fee = fields.Integer(string='# Payment')

    #partner_id = fields.Many2one('res.partner', string='Partner',  ondelete="cascade")

   
    #add field to check student type
    student_type=fields.Selection([('is_new_candidate','New Candidate'),('transfer_in','Transfer In Student')], default='is_new_candidate',required=True)
    
     #add fields to transfer in student
    major_id = fields.Many2one('hr.department', string='Major', domain=[('is_major', '=', True)], help="Select the Promote Major")
    division_id = fields.Many2one('education.division', string='Promote Program Year', help="Select the promote Program Year")
    
    #add fields for new candidate
    first_choice = fields.Many2one('hr.department', string="First Choice",
                             domain=[('can_enroll', '=', True) and ('is_major', '=', True)],
                            help="Choose Major to apply")
    second_choice = fields.Many2one('hr.department', string="Second Choice",
                            domain=[('can_enroll', '=', True) and ('is_major', '=', True)],
                            help="Choose Major to apply")
    third_choice = fields.Many2one('hr.department', string="Third Choice",
                             domain=[('can_enroll', '=', True) and ('is_major', '=', True)],
                            help="Choose Major to apply")
    forth_choice = fields.Many2one('hr.department', string="Forth Choice",
                           domain=[('can_enroll', '=', True) and ('is_major', '=', True)],
                            help="Choose Major to apply")
    fifth_choice = fields.Many2one('hr.department', string="Fifth Choice",
                            domain=[('can_enroll', '=', True) and ('is_major', '=', True)],
                            help="Choose Major to apply")
    student_id=fields.Char(string='Student ID.',  help="Enter Student ID of Student")
    roll_no = fields.Char(string='Seat_no in Matrix Exam', help="Enter Matriculation Exam Roll Number of Student")
    total_marks = fields.Char(string='Total Marks', help="Enter Matriculation Exam Total Marks of Student")
    
    _sql_constraints = [
        ('student_id', 'unique(student_id)', "Another Student already exists with this student_id !"),
    ]

    #add fields for parent's info
    f_nrc = fields.Char(string='Father NRC Number',  help="Enter Father NRC Number")
    m_nrc = fields.Char(string='Mother NRC Number',  help="Enter Mother NRC Number")
    f_nationality = fields.Many2one('res.country', string='Father Nationality', ondelete='restrict',
                                  help="Select the Father Nationality")
    m_nationality = fields.Many2one('res.country', string='Mother Nationality', ondelete='restrict',
                                  help="Select the Mother Nationality")
    f_occupation = fields.Char(string='Father Occupation',  help="Enter Father Occupation ")
    m_occupation = fields.Char(string='Mother Occupation', help="Enter Mother Occupation")
    f_religion = fields.Many2one('religion.religion', string="Father Religion", help="My Father Religion is ")
    m_religion = fields.Many2one('religion.religion', string="Mother Religion", help="My Mother Religion is ")    
    sibling_ids = fields.One2many('education.application.sibling', 'student_id', string="Student Sibling")

  

class StudentSiblings(models.Model):
    _name = 'education.application.sibling'
    #add fields for sibling's info
    name = fields.Char(string='Sibling Name',  help="Enter Sibling Name")
    nrc_no = fields.Char(string='Sibling NRC Number', help="Enter Sibling NRC Number")
    occupation = fields.Char(string='Sibling Occupation',  help="Enter Sibling Occupation ")
    address = fields.Char(string='Address',  help="Enter Sibling Address")
    student_id = fields.Many2one('education.application', string='Student')


class AssignMajor(models.TransientModel):
    _name = 'education.major_assign'
    #add to assign Major
    major_id = fields.Many2one('hr.department', string='Major', domain=[('is_major', '=', True)],
                                 help="Select Major to assign" )


    #modify major_id to student application (assign major to student)   
    @api.multi
    def assign_major(self,vals):        
        studnet_ids=vals['active_ids']
        #print(studnet_id)
        for rec in self:
            #print(rec.major_id)
            vals['major_id']=rec.major_id 
        for sid in studnet_ids:
            #print(sid)
            student_id = self.env['education.application'].browse(sid)
            if not student_id.major_id:
                student_id.major_id = vals['major_id']
                student_id.state ='major'
                self.env['education.application'].update(student_id)
            else:
                    raise ValidationError(_('These students have been already assigned major'))
            
        return
        
        
            

