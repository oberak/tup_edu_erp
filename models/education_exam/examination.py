
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class EducationExam(models.Model):
    _name = 'education.exam'
    _inherit = 'education.exam'
    
    division_id = fields.Many2one('education.class.division', string='Class',
                                    domain=lambda self: [('academic_year_id', '=', self.env['education.academic.year']._get_current_ay().id)]) # Rename Division to Class
    school_class_division_wise = fields.Selection([('division', 'Class')],
                                                  related='exam_type.school_class_division_wise')       # Remove exam type (Class)
    semester = fields.Many2one('education.semester', string='Semester',
                                       help="Select the Semester")  
    
    # add fields
    major_id = fields.Char(string="Major", readonly = True)                    
    pro_year = fields.Char(string='Program Year', readonly=True)

    # add function
    @api.onchange('division_id')
    def onchange_division_id(self):
        for rec in self:
            if self.env['education.class.division'].search([('name', '=', rec.division_id.name)]):
                obj = self.env['education.class.division'].browse(self.division_id.id)
                rec.pro_year = obj.division_id.name
                rec.major_id = obj.class_id.major_id.name
            return 

    # modify function
    @api.onchange('class_division_hider')
    def onchange_class_division_hider(self):
        self.school_class_division_wise = 'division'            #change :'school' to 'division'

class SubjectLine(models.Model):
    _inherit =  'education.subject.line'

    # modify field name
    mark = fields.Integer(string='Mark' , required=True)
  
class EducationExamType(models.Model):
    _name = 'education.exam.type'
    _inherit = 'education.exam.type'

    school_class_division_wise = fields.Selection([('division', 'PACT'), ('midterm', 'Midterm Exam'), ('final', 'Final Exam')],
                                                  string='Exam Type', default='division')           # Remove exam type (Class)