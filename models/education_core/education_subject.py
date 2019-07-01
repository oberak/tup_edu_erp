# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class EducationSubject(models.Model):
    _inherit = 'education.subject'    
    
    major_id = fields.Many2one('hr.department', string="Major",
                            required=True, help="Choose Major")
    is_language = fields.Boolean(string="Lecture", help="Tick if this subject is a lecture")
    is_tutorial = fields.Boolean(string='Tutorial', help="Tick if this is the Tutorial")
    is_class_work = fields.Boolean(string="Class Work", help="Tick if this is the class Work")
    # check logged user's department
    user_subjects=fields.Char(compute="_compute_user_subjects",search='user_subjects_search')

    @api.one
    @api.depends('major_id')
    def _compute_user_subjects(self):
        print('View my departemnt subjects')

    def user_subjects_search(self, operator, operand):
        employee_ids = self.env['hr.employee'].search([('user_id','in',self.env.user.login)]).ids
        return [('major_id.member_ids','in',employee_ids)]

class EducationSyllabus(models.Model):
    _name = 'education.syllabus'
    _inherit = 'education.syllabus'
    
    # modify fields
    name = fields.Char(string='Name', required = False)   # change to required = False

    # add fields
    major_id = fields.Many2one('hr.department', string="Major",
                            required=True, help="Choose Major")
    semester_id =fields.Many2one('education.semester', string="Semester" , required=True,
                    domain=lambda self: [('academic_year', '=', self.env['education.academic.year']._get_current_ay().id)])
    division_id = fields.Many2one('education.division', string='Program Year', required=True,
                                  help="Select the Program Year")
    description = fields.Text(string='Description')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Confirm')], default='draft')
    cur_ids = fields.One2many('education.curriculum', 'course_id', string="Curriculum") 
    # For logged user's department
    user_subjects=fields.Char(compute="_compute_user_subjects",search='user_subjects_search')  

    @api.one
    @api.depends('major_id')
    def _compute_user_subjects(self):
        print('View my departemnt subjects')
    
    def user_subjects_search(self, operator, operand):
        employee_ids = self.env['hr.employee'].search([('user_id','in',self.env.user.login)]).ids
        return [('major_id.member_ids','in',employee_ids)]

    # add functions
    # override for name
    @api.model
    def create(self, vals):
        """Return the name as a str of Major code + Program Year"""
        major_id = self.env['hr.department'].browse(vals['major_id'])
        division_id = self.env['education.division'].browse(vals['division_id'])
        name = str(major_id.major_code + '-' + division_id.name)
        vals['name'] = name
        return super(EducationSyllabus, self).create(vals)

    @api.multi
    def get_curriculum(self):
        for rec in self:
            if rec.major_id and rec.division_id and rec.semester_id:
                cur_ids = self.env['education.curriculum'].search([('major_id','=',rec.major_id.id),('program_year','=',rec.division_id.id),('semester_id','=',rec.semester_id.id)])
                if cur_ids:
                    for cur_id in cur_ids:
                        cur_id.course_id = self.id
                        data={
                            'course_id' : cur_id.course_id.id,
                        }
                        self.env['education.curriculum'].update(data)  
            rec.state ='done'

# add new classes      
class EducationCurriculum(models.Model):
    _name = 'education.curriculum'

    name = fields.Char(compute='get_name', default='New')
    course_title = fields.Many2one('education.subject', string='Subject')
    code = fields.Char('Code')
    lecture = fields.Integer('Lecture (hrs)')
    tutorial = fields.Integer('Tutorial (hrs)')
    practical = fields.Integer('Practical (hrs)')
    total = fields.Integer('Total')
    independent_learning = fields.Float('Independent Learning')
    credit_point = fields.Float('Credit Point')
    program_year =fields.Many2one('education.division', string='Program Year', required=True)
    major_id = fields.Many2one('hr.department', string="Major",
                            required=True, help="Choose Major")
    semester_id =fields.Many2one('education.semester', string="Semester" , required=True,
                    domain=lambda self: [('academic_year', '=', self.env['education.academic.year']._get_current_ay().id)])
    description = fields.Text(string='Description') 
    state = fields.Selection([('draft', 'Draft'), ('done', 'Confirm')], default='draft') 
    course_id = fields.Many2one('education.syllabus', string ='Courses', help = "Select the Courses")

    # For logged user's department
    user_subjects=fields.Char(compute="_compute_user_subjects",search='user_subjects_search')  

    @api.one
    @api.depends('major_id')
    def _compute_user_subjects(self):
        print('View my departemnt subjects')
    
    def user_subjects_search(self, operator, operand):
        employee_ids = self.env['hr.employee'].search([('user_id','in',self.env.user.login)]).ids
        return [('major_id.member_ids','in',employee_ids)]


    # Naming Class/Attendance_date
    def get_name(self):
        """To generate name for the model"""
        for i in self:
            i.name = str(i.program_year.name)+'-'+ str(i.major_id.major_code)+'-'+ str(i.course_title.name)


    @api.onchange('course_title')
    def _onchange_subject(self):
        for rec in self:
            rec.code = rec.course_title.code

    @api.multi
    def confirm_curriculum(self):
        for rec in self:
            rec.total = rec.lecture + rec.tutorial + rec.practical
            rec.independent_learning = rec.lecture * 2 + rec.tutorial * 0.5 + rec.practical * 0.5
            rec.credit_point = rec.lecture + rec.tutorial * 0.5 + rec.practical * 0.5
            rec.state = 'done'
    