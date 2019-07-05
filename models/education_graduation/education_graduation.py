from datetime import datetime
from dateutil import relativedelta
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class EducationGraduationClass(models.Model):
    _name = 'education.graduation.class'    
    _description = 'Graduation'

    name = fields.Char(compute='get_name')
    academic_year = fields.Many2one('education.academic.year', default=lambda self: self.env['education.academic.year']._get_current_ay(), 
                            string="Academic Year")
    class_id = fields.Many2one('education.class.division', string='Class')
    student_ids = fields.One2many('education.graduation', 'graduate_class_id', string="Research Record")

    def get_name(self):
        """To generate name for the model"""
        for i in self:
            i.name = str(i.academic_year.name)+'/'+str(i.class_id.name)

class EducationGraduation(models.Model):
    _name = 'education.graduation'    
    _description = 'Graduation'

    student_id = fields.Many2one('education.student', string='Student Name')
    nrc_no = fields.Char('Student NRC')
    f_name = fields.Char('Father Name')
    f_nrc_no = fields.Char('Father NRC')
    m_name = fields.Char('Mother Name')
    m_nrc_no = fields.Char('Mother NRC')
    address = fields.Char('Address')
    mobile = fields.Char('Mobile Number')
    email = fields.Char('Email')
    graduate_class_id = fields.Many2one('education.graduation.class', string='Graduation Class')

    def get_name(self):
        """To generate name for the model"""
        for i in self:
            i.name = str(i.student_id.name)


class GraduationStudent(models.Model):
    _name = 'graduation.student'
    # _inherit = ['mail.thread']
    # _inherits = {'res.partner': 'partner_id'}
    _description = 'Graduation Student Form'
    # _rec_name = 'name'
    

    name = fields.Char(compute='get_name')
    student_id = fields.Many2one('education.student', string='Student Name')
    graduated_year = fields.Char(string="Graduated Year" , required=True)
    # student_name = fields.Char( string='Student Name', required=True)
    nrc_no = fields.Char('Student NRC', required=True)
    f_name = fields.Char('Father Name', required=True)
    f_nrc_no = fields.Char('Father NRC', required=True)
    m_name = fields.Char('Mother Name')
    m_nrc_no = fields.Char('Mother NRC')
    email = fields.Char('Email')
    address = fields.Char('Current Address')
    per_address = fields.Char('Permanent Address')
    is_same_address = fields.Boolean(string="Permanent Address same as above", default=True,
                                     help="Tick the field if the Present and permanent address is same")
    phone = fields.Char('Phone No.', required=True)
    degree = fields.Selection([('B.Tech', 'B.Tech'),('B.E', 'B.E'), ('M.E', 'M.E'), ('Ph.D', 'Ph.D')],
                             default='draft', string='Degree' , required=True)
    ot_degree = fields.Char('Other Degree (if has)')
    apply_date = fields.Datetime('Apply Date', default=fields.Datetime.now, required=True)

    state = fields.Selection([('draft', 'Draft'), ('apply', 'Apply'), ('approve', 'Approve'),('cancel', 'Cancel'),('done', 'Done')],
                             default='draft')
    attend_or_not=fields.Selection([('attend','Attend'), ('not_attend','Not Attend')],default='attend', 
                string="Ceremony",required=True)
    receipt_count = fields.Integer(compute='_receipt_count', string='# Receipts') # for fee

    def get_name(self):
        """To generate name for the model"""
        for i in self:
            i.name = str(i.graduated_year)+' / '+ str(i.student_id.name)

    @api.one
    def apply(self, vals):
        for rec in self:
            if rec.nrc_no:
                obj=self.env['education.graduation'].search([('nrc_no','=',rec.nrc_no)])         
                if  not obj:
                    raise ValidationError(_('Cannot Apply!! Student has not been graduated yet'))            
                else :
                    rec.state='apply'
            return
    
    @api.multi
    def action_view_receipts(self):
        self.ensure_one()
        view = self.env.ref('education_fee.receipt_tree')
        domain = [('student_id', '=', self.student_id.id)]
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
            receipt_ids = self.env['account.invoice'].search([('student_id', '=', rec.student_id.id), ('state', '!=', 'cancel')])           
            rec.receipt_count = len(receipt_ids)    
    
    @api.multi
    def approve(self):
        """Approve all data"""
        for rec in self:
           rec.state = 'approve'

    @api.multi
    def cancel(self):
        """Cancel for the student application for graduation"""
        for rec in self:
            rec.state = 'cancel'
            rec.unlink()

    @api.multi
    def confirm(self):
        """Confirm Fee Payment for graduation"""
        for rec in self:
            if rec.receipt_count >= 1:
                rec.state = 'done'