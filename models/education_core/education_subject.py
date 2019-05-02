# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class EducationSubject(models.Model):
    _inherit = 'education.subject'    
    
    major_id = fields.Many2one('hr.department', string="Major",
                            required=True, domain=[('is_major', '=', True)],
                            help="Choose Major")
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
                            required=True, domain=[('is_major', '=', True)],
                            help="Choose Major")

    division_id = fields.Many2one('education.division', string='Program Year', required=True,
                                  help="Select the Program Year") 
    syllabus_ids = fields.One2many('education.syllabuses', 'syllabus_id', string="Syllabus")   

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

    # override for name
    @api.multi
    @api.depends('major_id', 'division_id')
    def write(self, vals):
        """Return the name as a str of Major code + Program Year"""
        for rec in self:
            major_code = rec.major_id.major_code
            name = rec.division_id.name
            if 'major_id' in vals:
                major_code = self.env['hr.department'].browse(vals['major_id']).major_code
            if 'division_id' in vals:
                name = self.env['education.division'].browse(vals['division_id']).name
            vals['name'] = str(major_code + '-' + name)
        return super(EducationSyllabus, self).write(vals)


# add new classes      
class EducationSyllabuses(models.Model):
    _name = 'education.syllabuses'

    subject_id = fields.Many2one('education.subject', string='Subject')
    lecture_hour = fields.Char(string="Lecture (hrs)", required=True, help="Pick lecture hours")
    tutorial_hour = fields.Char(string="Tutorial (hrs)", help="Pick Tutorial hours")
    practical_hour = fields.Char(string="Practical (hrs)", help="Pick Practical hours")
    classwork_hour = fields.Char(string="Class Work (hrs)",  help="Pick Class Work hours") 
    syllabus_id = fields.Many2one('education.syllabus', string ='Syllabus', help = "Select the Syllabus")  
        
    @api.onchange('subject_id')
    def onchange_subject(self):
        for rec in self:
            if rec.subject_id.is_language:
                rec.lecture_hour = ""
            if rec.subject_id.is_tutorial:
                rec.tutorial_hour = "" 
            if rec.subject_id.is_lab:
                rec.practical_hour = "" 
            if rec.subject_id.is_class_work:
                rec.classwork_hour = ""