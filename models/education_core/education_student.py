from odoo import fields, models, _, api
from odoo.exceptions import ValidationError

class EducationStudent(models.Model):
    _name = 'education.student'
    _inherit = 'education.student'
    _description = 'Student Form'
        
    @api.multi
    def action_view_receipts(self):
        self.ensure_one()
        view = self.env.ref('education_fee.receipt_tree')
        domain = [('student_id', '=', self.id)]
        return {
            'name': _('Receipts'),
            'domain': domain,
            'res_model': 'account.invoice',
            'type': 'ir.actions.act_window',
            'view_id': view.id,
            'view_mode': 'tree',
            'view_type': 'form',
            'limit': 80,
        }

    @api.multi
    def _receipt_count(self):
        """Return the count of the receipts"""
        for rec in self:
            receipt_ids = self.env['account.invoice'].search([('student_id', '=', rec.id), ('state', '!=', 'cancel')])
            rec.receipt_count = len(receipt_ids)

    #add fields
    nrc_no = fields.Char(string='NRC Number', required=True, help="Enter NRC Number of Student")
    is_registered = fields.Boolean(string="Check Signup", default=False)
    student_id=fields.Char(string='Student ID.',  help="Enter Student ID of Student")
    major_id = fields.Many2one('hr.department', string="Major",
                            required=True, domain=[('is_major', '=', True)],
                            help="Choose Major")
    sibling_ids = fields.One2many('education.student.sibling', 'student_id', string="Student Sibling")
    receipt_count = fields.Integer(compute='_receipt_count', string='# Receipts') # for fee

    _sql_constraints = [
        ('nrc_no_uniq', 'unique(nrc_no)', "Another Student already exists with this NRC No !"),
        ('student_id_uniq', 'unique(student_id)', "Another Student already exists with this student_id !")
    ]
    #add status about the state of student    
    state = fields.Selection([('in_school', 'In School'),('transfer_out', 'Transfer Out'), ('leave', 'Leave'),('expel', 'expel'),('drop_off', 'Drop Off'),('graduate', 'Graduate')],
                             string='State', default='in_school', track_visibility='onchange')

    #modify fields
    medium = fields.Many2one('education.medium', string="Medium", required=False)
    sec_lang = fields.Many2one('education.subject', string="Second language", required=False, domain=[('is_language', '=', True)])
    mother_tongue = fields.Many2one('education.mother.tongue', string="Mother Tongue", required=False, domain=[('is_language', '=', True)])
    blood_group = fields.Selection([('a+', 'A+'), ('a-', 'A-'), ('b+', 'B+'), ('o+', 'O+'), ('o-', 'O-'),
                                    ('ab-', 'AB-'), ('ab+', 'AB+')],
                                   string='Blood Group', required=False, default='a+', track_visibility='onchange')

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

class EducationStudentSiblings(models.Model):
    _name = 'education.student.sibling'
    #add fields for sibling's info
    name = fields.Char(string='Sibling Name',  help="Enter Sibling Name")
    nrc_no = fields.Char(string='Sibling NRC Number', help="Enter Sibling NRC Number")
    occupation = fields.Char(string='Sibling Occupation',  help="Enter Sibling Occupation ")
    address = fields.Char(string='Address',  help="Enter Sibling Address")
    student_id = fields.Many2one('education.student', string='Student')

class SetStudentState(models.TransientModel):
    _name = 'education.student.state'
    #add to state of student
    student_state = fields.Selection([('drop_off', 'Drop Off'), ('transfer_out', 'Transfer Out'), ('expel', 'Expel'), ('leave', 'Leave')],string='Student State',  track_visibility='onchange')
    
    #modify state of student  
    @api.multi
    def set_student_state(self,vals):        
        student_ids=vals['active_ids']        
        for rec in self:           
            vals['student_state']=rec.student_state 
        for sid in student_ids:            
            student_id = self.env['education.student'].browse(sid)          
            student_id.state = vals['student_state']                
            self.env['education.student'].update(student_id)
        return
    