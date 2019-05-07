from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class EducationExam(models.Model):
    _name = 'education.exam'
    _inherit = 'education.exam'
    
    division_id = fields.Many2one('education.class.division', string='Class') # Rename Division to Class
    school_class_division_wise = fields.Selection([('division', 'Class')],
                                                  related='exam_type.school_class_division_wise')       # Remove exam type (Class)

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

class EducationExamType(models.Model):
    _name = 'education.exam.type'
    _inherit = 'education.exam.type'

    school_class_division_wise = fields.Selection([('division', 'Class'), ('final', 'Final Exam (Exam that promotes students to the next class)')],
                                                  string='Exam Type', default='division')           # Remove exam type (Class)
    