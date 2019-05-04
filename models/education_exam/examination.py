from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class EducationExam(models.Model):
    _name = 'education.exam'
    _inherit = 'education.exam'
    
    division_id = fields.Many2one('education.class.division', string='Class') # Rename Division to Class
    school_class_division_wise = fields.Selection([('school', 'School'), ('division', 'Class')],
                                                  related='exam_type.school_class_division_wise')           # Remove exam type (Class)
 

class EducationExamType(models.Model):
    _name = 'education.exam.type'
    _inherit = 'education.exam.type'

    school_class_division_wise = fields.Selection([('school', 'School'), ('division', 'Class'), ('final', 'Final Exam (Exam that promotes students to the next class)')],
                                                  string='Exam Type', default='division')           # Remove exam type (Class)
    