# -*- coding: utf-8 -*-

from odoo import fields, models, _, api
from odoo.exceptions import ValidationError

class StudentApplication(models.Model):
    _name = 'education.application'
    _inherit = 'education.application'
    #_order = 'total_marks desc'
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
    
    # Override method for res.partner
    @api.multi
    def send_to_verify(self):
        """Button action for sending the application for the verification"""
        for rec in self:
            document_ids = self.env['education.documents'].search([('application_ref', '=', rec.id)])
            if not document_ids:
                raise ValidationError(_('No Documents provided'))
            rec.write({
                'state': 'verification'
            })
            # create partner for fee
            values = {
                'name': rec.name,
                'street': rec.street,
                'street2': rec.street2,
                'email': rec.email,
                'mobile': rec.mobile,
                'phone': rec.phone,
            }
            partner = self.env['res.partner'].create(values)
            rec.partner_id = partner.id
        
    #This function is triggered when the user clicks on the button 'Payment for Tution Fee'
    @api.one
    def paid_fee(self):
        # TODO: move this logic to payment
        for rec in self:
            if rec.student_type == 'is_new_candidate':
                rec.write({
                'state': 'fee'
                })
            else:
                rec.state = 'approve'

    #This function is triggered when the user clicks on the button 'Assign Major'
    @api.one
    def assign_major(self, vals):
        for rec in self:
            vals['major_id']=rec.major_id
            rec.state='major'
            self.env['education.application'].update(vals)            
        return

   #overwriting 'create student' function and assign class to student
    @api.multi
    def create_student(self,vals):
        """Create student from the application and data and return the student"""
        for rec in self:
            #add student ID automatically 
            sid = 5578 + rec.id            
            sid = str(sid)
            student_id='ptntu - 00'+sid  

            # automatically assign class to student depends on academic_year and major , (for transfer in) division_id
            if rec.student_type == 'is_new_candidate':
                c_id = self.env['education.class'].search(['&',('ay_id', '=',rec.academic_year_id.id),('major_id', '=', rec.major_id.id)]).id         
                class_id = self.env['education.class.division'].search([('class_id', '=', c_id),('division_id', '=', '1BE')]).id
            else :
                c_id = self.env['education.class'].search(['&',('ay_id', '=',rec.academic_year_id.id),('major_id', '=', rec.major_id.id)]).id         
                class_id = self.env['education.class.division'].search(['&',('class_id', '=', c_id),('division_id', '=', rec.division_id.id)]).id

            vals['class_id']=class_id
            self.env['education.application'].update(vals['class_id'])
            if not class_id:
                raise ValidationError(_('There is no class for this student !! Need to create class first '))         
           
            values = {
                'name': rec.name,
                'last_name': rec.last_name,
                'middle_name': rec.middle_name,
                'application_id': rec.id,
                'nrc_no': rec.nrc_no,
                'student_id': student_id,
                'father_name': rec.father_name,
                'mother_name': rec.mother_name,
                'street': rec.street,
                'street2': rec.street2,
                'city': rec.city,
                'state_id': rec.state_id.id,
                'country_id': rec.country_id.id,
                'zip': rec.zip,
                'is_same_address': rec.is_same_address,
                'per_street': rec.per_street,
                'per_street2': rec.per_street2,
                'per_city': rec.per_city,
                'per_state_id': rec.per_state_id.id,
                'per_country_id': rec.per_country_id.id,
                'per_zip': rec.per_zip,
                'gender': rec.gender,
                'date_of_birth': rec.date_of_birth,
                'blood_group': rec.blood_group,
                'nationality': rec.nationality.id,
                'email': rec.email,
                'mobile': rec.mobile,
                'phone': rec.phone,
                'image': rec.image,
                'is_student': True,
                'religion_id': rec.religion_id.id,                
                'major_id' : rec.major_id.id,
                'mother_tongue': rec.mother_tongue.id,              
                'class_id': class_id,
                'f_nrc': rec.f_nrc,
                'f_nationality':rec.f_nationality.id,
                'f_occupation':rec.f_occupation,
                'f_religion': rec.f_religion.id,
                'm_nrc': rec.m_nrc,
                'm_nationality':rec.m_nationality.id,
                'm_occupation':rec.m_occupation,
                'm_religion': rec.m_religion.id,
                'partner_id': rec.partner_id.id, # for fee
            }            
            if not rec.is_same_address:
                pass
            else:
                values.update({
                    'per_street': rec.street,
                    'per_street2': rec.street2,
                    'per_city': rec.city,
                    'per_state_id': rec.state_id.id,
                    'per_country_id': rec.country_id.id,
                    'per_zip': rec.zip,
                })

            student = self.env['education.student'].create(values)

            # add subling infos to the student
            stu_id= self.env['education.student'].search([])[-1].id
            if rec.sibling_ids:
                sibling_ids=rec.sibling_ids                
                for sid in sibling_ids:
                    self.env['education.student.sibling'].create({
                        'name' : sid.name,
                        'nrc_no' : sid.nrc_no,
                        'occupation' : sid.occupation,
                        'address' : sid.address,
                        'student_id' : stu_id,                        
                    })   
            
            rec.write({
                'state': 'done',
                'class_id' : class_id
            })
            return {
                'name': _('Student'),
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'education.student',
                'type': 'ir.actions.act_window',
                'res_id': student.id,
                'context': self.env.context
            }
   
    # add fields
    nrc_no = fields.Char(string='NRC Number', required=True, help="Enter NRC Number of Student")
    is_registered = fields.Boolean(string="Check Signup", default=False)
    partner_id = fields.Many2one('res.partner', string='Partner',  ondelete="cascade") # for fee

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

    # add field for creating student
    class_id = fields.Many2one('education.class.division', string='Class')
    
    #modify status 
    state = fields.Selection([('draft', 'Draft'), ('apply', 'Apply'),('verification', 'Verify'),('fee', 'Tution Fee'),('major', 'Assign Major'),
                              ('approve', 'Approve'), ('reject', 'Reject'), ('done', 'Done')],
                             string='State', default='draft', track_visibility='onchange')
    
    #add fields for payment
    #payment_fee = fields.Integer(string='# Payment')

   
    #add field to check student type
    student_type=fields.Selection([('is_new_candidate','New Candidate'),('transfer_in','Transfer In Student')], default='is_new_candidate',required=True)
    
     #add fields to transfer in student
    major_id = fields.Many2one('hr.department', string='Major', domain=[('is_major', '=', True)], help="Select the Major")
    division_id = fields.Many2one('education.division', string='Program Year', help="Select the Program Year")
    
    #add fields for new candidate
    first_choice = fields.Many2one('hr.department', string="First Choice",
                             domain=[('is_major', '=', True)],
                            help="Choose Major to apply")
    second_choice = fields.Many2one('hr.department', string="Second Choice",
                            domain=[('is_major', '=', True)],
                            help="Choose Major to apply")
    third_choice = fields.Many2one('hr.department', string="Third Choice",
                             domain=[('is_major', '=', True)],
                            help="Choose Major to apply")
    forth_choice = fields.Many2one('hr.department', string="Forth Choice",
                           domain=[('is_major', '=', True)],
                            help="Choose Major to apply")
    fifth_choice = fields.Many2one('hr.department', string="Fifth Choice",
                            domain=[('is_major', '=', True)],
                            help="Choose Major to apply")
    admission_no=fields.Char(string='Admission No.',  help="Enter Student ID of Student")
    roll_no = fields.Char(string='Seat_no in Matrix Exam', help="Enter Matriculation Exam Roll Number of Student")
    total_marks = fields.Char(string='Total Marks', help="Enter Matriculation Exam Total Marks of Student")
    
    _sql_constraints = [
        ('admission_no', 'unique(admission_no)', "Another Student already exists with this admission_no !"),
    ]

    #add fields for parent's info
    f_nrc = fields.Char(string='Father NRC Number',  help="Enter Father NRC Number")
    m_nrc = fields.Char(string='Mother NRC Number',  help="Enter Mother NRC Number")
    f_nationality = fields.Many2one('res.country', string='Father Nationality', ondelete='restrict',
                                  help="Select the Father Nationality" , default=145)
    m_nationality = fields.Many2one('res.country', string='Mother Nationality', ondelete='restrict',
                                  help="Select the Mother Nationality", default=145)
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
            if  student_id.state == 'fee':
                student_id.major_id = vals['major_id']
                student_id.state ='major'
                self.env['education.application'].update(student_id)
            else:
                    raise ValidationError(_('Assigning major to the student is not permitted'))
            
        return
        
        
            

