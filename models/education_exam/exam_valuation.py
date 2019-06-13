from odoo import models, fields, api, _
from odoo.exceptions import UserError

class EducationExamValuation(models.Model):
    _name = 'education.exam.valuation'
    _inherit = 'education.exam.valuation'

    # modify fields
    class_id = fields.Many2one('education.class', string='Class', required=False)
    division_id = fields.Many2one('education.class.division', string='Class', required=False,
                                domain=lambda self: [('academic_year_id', '=', self.env['education.academic.year']._get_current_ay().id)]) # change name : Division to Class

    # add fields
    major_id = fields.Char(string="Major", readonly=True)                    
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

    # modify function : add two (pro_year , major_id)
    @api.multi
    def valuation_completed(self):
        self.name = str(self.exam_id.exam_type.name) + '-' + str(self.exam_id.start_date)[0:10] + ' (' + str(
            self.division_id.name) + ')'
        result_obj = self.env['education.exam.results']
        result_line_obj = self.env['results.subject.line']
        for students in self.valuation_line:
            search_result = result_obj.search(
                [('exam_id', '=', self.exam_id.id), ('division_id', '=', self.division_id.id),
                 ('student_id', '=', students.student_id.id)])
            if len(search_result) < 1:
                result_data = {
                    'name': self.name,
                    'exam_id': self.exam_id.id,
                    'class_id': self.class_id.id,
                    'division_id': self.division_id.id,
                    'student_id': students.student_id.id,
                    'student_name': students.student_id.name,
                    'pro_year' : self.pro_year,
                    'major_id' : self.major_id,
                }
                result = result_obj.create(result_data)
                result_line_data = {
                    'name': self.name,
                    'subject_id': self.subject_id.id,
                    'max_mark': self.mark,
                    'pass_mark': self.pass_mark,
                    'mark_scored': students.mark_scored,
                    'pass_or_fail': students.pass_or_fail,
                    'result_id': result.id,
                    'exam_id': self.exam_id.id,
                    'class_id': self.class_id.id,
                    'division_id': self.division_id.id,
                    'student_id': students.student_id.id,
                    'student_name': students.student_id.name,
                }
                result_line_obj.create(result_line_data)
            else:
                result_line_data = {
                    'subject_id': self.subject_id.id,
                    'max_mark': self.mark,
                    'pass_mark': self.pass_mark,
                    'mark_scored': students.mark_scored,
                    'pass_or_fail': students.pass_or_fail,
                    'result_id': search_result.id,
                    'exam_id': self.exam_id.id,
                    'class_id': self.class_id.id,
                    'division_id': self.division_id.id,
                    'student_id': students.student_id.id,
                    'student_name': students.student_id.name,
                }
                result_line_obj.create(result_line_data)
        self.state = 'completed'
    
  
