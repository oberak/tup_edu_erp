from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class EducationExamResults(models.Model):
    _inherit = 'education.exam.results'

    division_id = fields.Many2one('education.class.division', string='Class',
                                domain=lambda self: [('academic_year_id', '=', self.env['education.academic.year']._get_current_ay().id)])  # Rename Division to Class

    # add fields
    major_id = fields.Char(string="Major")                    
    pro_year = fields.Char(string='Program Year')

class ResultsSubjectLine(models.Model):
    _inherit = 'results.subject.line'

    division_id = fields.Many2one('education.class.division', string='Class') # Rename Division to Class

class SubjectOverallResults(models.Model):
    _name = 'education.subject.overallresults'

    name = fields.Char(compute='get_name', string='Name', default='New')
    class_division = fields.Many2one('education.class.division', string='Class') 
    student_id = fields.Many2one('education.student',string = 'Student')
    overall_marks = fields.Float(string='Total Score', store=True, readonly=True)
    results_line = fields.One2many('education.subject.overallresult.line', 'result_line_id', string='Result Line')
    subject_id = fields.Many2one('education.subject', string='Subject')
    total_given_marks = fields.Float(string='Total Given Marks' , readonly=True)
    total_pass_marks = fields.Float(string='Overall Pass Marks')
    actual_mark = fields.Float(string='Avearage Score', store=True, readonly=True)
    pass_or_fail = fields.Boolean(string='Pass/Fail')
    state = fields.Selection([('draft','Draft'),('done','Completed')], string='State',required=True, default='draft',track_visibility='onchange')
    overall_result_id = fields.Many2one('education.overall.exam.result',string='Subjects')

    def get_name(self):
        """To generate name for the model"""
        for i in self:
            i.name = str(i.class_division.name)+ "/" + str(i.subject_id.name) + "/" + str(i.student_id.name)+ "/ Result" 

    @api.model
    def create(self, vals):
        res = super(SubjectOverallResults, self).create(vals)
        already_created =  self.env['education.subject.overallresults'].search([('class_division','=',res.class_division.id),('student_id','=', res.student_id.id),('subject_id','=', res.subject_id.id)])
        if len(already_created) > 1:
            raise ValidationError(
                _('Result "%s and %s" of %s is already created', ) % (res.class_division.name,res.subject_id.name,res.student_id.name))
        return res

    @api.onchange('class_division')
    def onchange_class_division(self):
        """Gets the students"""
        for record in self:
            obj = self.env['education.student'].search([('class_id', '=', record.class_division.id)])
            obj1 = self.env['education.timetable.schedule'].search([('class_division', '=', record.class_division.id)])            
            student_list = []
            subject_list = []
            if obj :
                for stu_id in obj:                   
                    student_list.append(stu_id.id)           
            if obj1:
                for sub_id in obj1:
                        subject_list.append(sub_id.subject.id)
            vals = {
                    'domain': {
                        'subject_id': [('id', 'in', subject_list)],
                        'student_id': [('id', 'in', student_list)]
                }
            }
            return vals 

    def get_overall_results(self):
        overall_marks = 0.0
        total_marks = 0.0
        for record in self:
            obj = self.env['results.subject.line'].search([('division_id','=',record.class_division.id),('student_id','=', record.student_id.id),('subject_id','=', record.subject_id.id)])
            obj1 = self.env['education.exam.valuation'].search([('division_id','=',record.class_division.id),('subject_id','=', record.subject_id.id)])
            if obj1:
                for rec in obj1:
                    total_marks += rec.mark
            if obj :
                for result in obj:
                    overall_marks += result.mark_scored
                    data = {
                        'class_division': record.class_division.id,
                        'subject_id':record.subject_id.id,
                        'student_id': record.student_id.id,
                        'exam_id':result.exam_id.id,
                        'total_marks':result.mark_scored,
                        'result_line_id':self.id,
                        'pass_or_fail' : result.pass_or_fail,
                    }
                    self.env['education.subject.overallresult.line'].create(data)
            record.overall_marks=overall_marks
            record.total_given_marks = total_marks
            record.actual_mark = overall_marks *100 / record.total_given_marks
            if record.actual_mark >= record.total_pass_marks:
                self.pass_or_fail = True
            else:
                self.pass_or_fail = False
            record.state='done'

class SubjectOverallResultsLine(models.Model):
    _name = 'education.subject.overallresult.line'

    class_division = fields.Many2one('education.class.division', string='Class') 
    student_id = fields.Many2one('education.student',string = 'Student')
    exam_id = fields.Many2one('education.exam',string= 'Exam')  
    subject_id = fields.Many2one('education.subject',string='Subject')  
    total_marks=fields.Float(string='Score')
    result_line_id = fields.Many2one('education.overallexam.results', string='Result Id')
    pass_or_fail = fields.Boolean(string='Pass/Fail')

class ExamOverallResultsLine(models.Model):
    _name = 'education.overall.exam.result'

    name = fields.Char(compute='get_name', string='Name', default='New')
    class_division = fields.Many2one('education.class.division', string='Class') 
    student_id = fields.Many2one('education.student',string = 'Student')
    state = fields.Selection([('draft','Draft'),('done','Completed')], string='State',required=True, default='draft',track_visibility='onchange')
    result_ids = fields.One2many('education.subject.overallresults','overall_result_id',string='Result Ids')
    total_avg_score = fields.Integer(string='Total Average Score', readonly= True)
    pass_or_fail = fields.Boolean(string='Pass/Fail')
   
    def get_name(self):
        """To generate name for the model"""
        for i in self:
            i.name = str(i.class_division.name)+ "/" + str(i.student_id.name)+ "/ Result" 

    @api.onchange('class_division')
    def onchange_class_division(self):
        """Gets the students"""
        for record in self:
            obj = self.env['education.student'].search([('class_id', '=', record.class_division.id)])                   
            student_list = []
            if obj :
                for stu_id in obj:                   
                    student_list.append(stu_id.id)           
           
            vals = {
                    'domain': {                        
                        'student_id': [('id', 'in', student_list)]
                }
            }
            return vals 
    
    def get_overall_exam_results(self):
        total_marks = 0.0
        check = True
        for record in self:
            obj = self.env['education.subject.overallresults'].search([('class_division','=',record.class_division.id),('student_id','=', record.student_id.id)])
            if obj:
                for res in obj:
                    total_marks += res.actual_mark
                    if res.pass_or_fail == True:
                        check = True
                    else:
                        check = False
                    res.overall_result_id=self.id
                    r_id=res.overall_result_id
                    data={
                        'overall_result_id':r_id.id,
                    }
                    self.env['education.subject.overallresults'].update(data)
            if check == True:
                record.pass_or_fail = True
            else:
                record.pass_or_fail = False
            record.total_avg_score = total_marks
            record.state='done'
                    
                   
    

