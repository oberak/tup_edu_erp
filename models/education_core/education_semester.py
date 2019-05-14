# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
from datetime import datetime

class EducationSemester(models.Model):
    _name = 'education.semester'
    _description = 'Semester'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(compute='get_name')
    semester = fields.Selection([('1st Semester', '1st Semester'), ('2nd Semester', '2nd Semester')], default='seme1')
    seme_start_date = fields.Date(string='Start date', required=True, help='Starting date of semester')
    seme_end_date = fields.Date(string='End date', required=True, help='Ending of semester')
    seme_description = fields.Text(string='Description', help="Description about the semester")
    academic_year = fields.Many2one('education.academic.year', string='Academic Year',
                                       help="Select the Academic Year", required=True)    
    # seme_code = fields.Char(string='Code', required=True, help='Code of semester')
    # sequence = fields.Integer(string='Sequence', required=True)

    def get_name(self):
        """To generate name for the model"""
        for i in self:
            i.name = str(i.semester) + "(" + str(i.academic_year.name) +")"
    
    @api.constrains('seme_start_date', 'seme_end_date')
    def validate_date(self):
        """Checking the start and end dates of the syllabus,
        raise warning if start date is not anterior"""
        for rec in self:
            if rec.seme_start_date >= rec.seme_end_date:
                raise ValidationError(_('Start date must be Anterior to End date'))
    
    @api.model
    def _get_current_semester(self):
        domain = [
            ('seme_start_date', '<=', datetime.now().strftime('%Y-%m-%d')),
            ('seme_end_date', '>=', datetime.now().strftime('%Y-%m-%d')),
        ]
        return self.search(domain, limit=1)