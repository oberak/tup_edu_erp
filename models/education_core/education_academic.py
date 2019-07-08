# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class EducationAcademic(models.Model):
    _inherit = 'education.academic.year'

    #modify fields
    sequence = fields.Integer(string='Sequence', required=False)
    ay_code = fields.Char(string='Code', required=False, help='Code of academic year', readonly=True)
    active = fields.Boolean(string='Active', default=True)
    no_students= fields.Integer(compute='_get_student_count', string='Number of student')
  
    def _get_student_count(self):
        """Return the number of students in the class"""
        for rec in self:
            students = self.env['education.application'].search([('academic_year_id', '=', rec.id)])
            student_count = len(students) if students else 0
            rec.update({
                'no_students': student_count
            })
    @api.model
    def _get_current_ay(self):
        domain = [
            ('ay_start_date', '<=', datetime.now().strftime('%Y-%m-%d')),
            ('ay_end_date', '>=', datetime.now().strftime('%Y-%m-%d')),
        ]
        return self.search(domain, limit=1)

    # override for code
    @api.model
    def create(self, vals):
        """Return the code as a left four digit of Application Year"""        
        vals['ay_code'] = vals['name'][:4]
        return super(EducationAcademic, self).create(vals)

    #override for code
    @api.one
    @api.depends('name')
    def write(self, vals):
        if 'name' in vals:
            vals['ay_code'] = vals['name'][:4]
        vals['ay_code'] = vals['ay_code']
        return super(EducationAcademic, self).write(vals)

class EducationAcademicCalendar(models.Model):
    _name = 'education.academic.calendar'

    ay_id = fields.Many2one('education.academic.year', string='Academic Year', required=True, 
                            help="Select the Academic Year")
    start_date = fields.Date(string='Start date', required=True, help='Starting date of academic year')
    end_date = fields.Date(string='End date', required=True, help='Ending of academic year')
    period = fields.Char('Duration', help='how long have taken')
    description = fields.Text(string='Description', help="Description about the academic year")

   
