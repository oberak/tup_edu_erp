from odoo import fields, models, _, api
from odoo.exceptions import ValidationError

class EducationStudent(models.Model):
    _name = 'education.student'
    _inherit = 'education.student'
    _description = 'Student Form'

    #action for drop_off student
    @api.multi
    def drop_off(self):
        active_ids = self.ids
        for sid in active_ids:            
            s_id = self.env['education.student'].browse(sid)
            s_id.state = "drop_off"
            print(s_id.state)           
        return 

    #action for transfer_out student
    @api.multi
    def transfer_out(self):
        active_ids = self.ids
        for sid in active_ids:            
            s_id = self.env['education.student'].browse(sid)
            s_id.state = "transfer_out"
            print(s_id.state)           
        return 
    
    #action for leave student
    @api.multi
    def leave(self):
        active_ids = self.ids
        for sid in active_ids:            
            s_id = self.env['education.student'].browse(sid)
            s_id.state = "leave"
            print(s_id.state)           
        return 
    
    #action for expel student
    @api.multi
    def expel(self):
        active_ids = self.ids
        for sid in active_ids:            
            s_id = self.env['education.student'].browse(sid)
            s_id.state = "expel"
            print(s_id.state)           
        return 
    
   
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

    #add field 
    name = fields.Char('Name')
    nrc_no = fields.Char(string='NRC Number', required=True, help="Enter NRC Number of Student")
    is_registered = fields.Boolean(string="Check Signup", default=False)
    student_id=fields.Char(string='Student ID.',  help="Enter Student ID of Student")
    major_id = fields.Many2one('hr.department', string="Major",
                            required=True, domain=[('is_major', '=', True)],
                            help="Choose Major")
    sibling_ids = fields.One2many('education.student.sibling', 'student_id', string="Student Sibling")
    receipt_count = fields.Integer(compute='_receipt_count', string='# Receipts') # for fee
    
    #add status about the state of student    
    state = fields.Selection([('in_school', 'In School'),('transfer_out', 'Transfer Out'), ('leave', 'Leave'),('expel', 'expel'),('drop_off', 'Drop Off'),('graduate', 'Graduate')],
                             string='State', default='in_school', track_visibility='onchange')


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

class EducationStudentSiblings(models.Model):
    _name = 'education.student.sibling'
    #add fields for sibling's info
    name = fields.Char(string='Sibling Name',  help="Enter Sibling Name")
    nrc_no = fields.Char(string='Sibling NRC Number', help="Enter Sibling NRC Number")
    occupation = fields.Char(string='Sibling Occupation',  help="Enter Sibling Occupation ")
    address = fields.Char(string='Address',  help="Enter Sibling Address")
    student_id = fields.Many2one('education.student', string='Student')


  

    