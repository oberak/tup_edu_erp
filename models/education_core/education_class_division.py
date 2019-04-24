# -*- coding: utf-8 -*-

from odoo.exceptions import ValidationError
from odoo import fields, models, api, _

class EducationClass(models.Model):
    _inherit = 'education.class'
    _description = "Batch : Application Year + Major code"

    # Modify fields name
    name = fields.Char(string='Batch Name', readonly=True) # rename Class to Batch

    # add fields for name
    ay_id = fields.Many2one('education.academic.year', string='Academic Year', required=True, help="Select the Academic Year")
    major_id = fields.Many2one('hr.department', string='Major', required=True, domain=[('is_major', '=', True)], help="Select the Major")

    # add unique constraint for name
    _sql_constraints = [ ('name', 'unique (name)','Batch already exists for the Academic year and the Major!') ]
    # syllabus_ids = fields.One2many('education.syllabus', 'class_id')
    # division_ids = fields.One2many('education.division', 'class_id')

    # override for name
    @api.model
    def create(self, vals):
        """Return the name as a str of Application Year + Major code"""
        ay_id = self.env['education.academic.year'].browse(vals['ay_id'])
        major_id = self.env['hr.department'].browse(vals['major_id'])
        name = str(ay_id.ay_code + '-' + major_id.major_code)
        vals['name'] = name
        return super(EducationClass, self).create(vals)

    # override for name
    @api.multi
    @api.depends('ay_id', 'major_id')
    def write(self, vals):
        """Return the name as a str of Application Year + Major code"""
        for rec in self:
            ay_code = rec.ay_id.ay_code
            major_code = rec.major_id.major_code
            if 'ay_id' in vals:
                ay_code = self.env['education.academic.year'].browse(vals['ay_id']).ay_code
            if 'major_id' in vals:
                major_code = self.env['hr.department'].browse(vals['major_id']).major_code
            vals['name'] = str(ay_code + '-' + major_code)
        return super(EducationClass, self).write(vals)


class EducationDivision(models.Model):
    _inherit = 'education.division'
    _description = "Program Year"

    # Modify fields name
    name = fields.Char(string='Program Year', required=True, help="Enter the Program Year") # rename Division to Program Year
    # strength = fields.Integer(string='Class Strength', help="Total strength of the class")
    # faculty_id = fields.Many2one('education.faculty', string='Class Faculty', help="Class teacher/Faculty")
    # class_id = fields.Many2one('education.class', string='Class')


class EducationClassDivision(models.Model):
    _inherit = 'education.class.division'
    _description = "Class: Batch + Program Year"

    # Modify fields name
    #name = fields.Char(string='Name', readonly=True)
    class_id = fields.Many2one('education.class', string='Batch', required=True,
                               help="Select the Batch") # rename Class to Batch
    division_id = fields.Many2one('education.division', string='Program Year', required=True,
                                  help="Select the Program Year") # rename Division to Program year
    #actual_strength = fields.Integer(string='Class Strength', help="Total strength of the class")
    #faculty_id = fields.Many2one('education.faculty', string='Class Faculty', help="Class teacher/Faculty")
    #academic_year_id = fields.Many2one('education.academic.year', string='Academic Year',
    #                                   help="Select the Academic Year", required=True)
    #student_ids = fields.One2many('education.student', 'class_id', string='Students')
    #amenities_ids = fields.One2many('education.class.amenities', 'class_id', string='Amenities')
    #student_count = fields.Integer(string='Students Count', compute='_get_student_count')

class EducationClassDivisionHistory(models.Model):
    _inherit = 'education.class.history'
    _description = "Class history"
    _rec_name = 'class_id'

    # Modify fields name
    class_id = fields.Many2one('education.class.division', string='Batch',
                               help="Select the Batch") # rename Class to Batch
    #academic_year_id = fields.Many2one('education.academic.year', string='Academic Year',
    #                                   help="Select the Academic Year")
    #student_id = fields.Many2one('education.student', string='Students')
