from datetime import datetime
from dateutil import relativedelta
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class EducationPromotion(models.Model):
    _name = 'education.graduation'    
    _description = 'Graduation'

    name = fields.Char(compute='get_name')
    academic_year = fields.Many2one('education.academic.year', default=lambda self: self.env['education.academic.year']._get_current_ay(), 
                            string="Academic Year")
    class_id = fields.Many2one('education.class.division', string='Class')
    student_id = fields.Many2one('education.student', string='Student Name')
    nrc_no = fields.Char('Student NRC')
    f_name = fields.Char('Father Name')
    f_nrc_no = fields.Char('Father NRC')
    m_name = fields.Char('Mother Name')
    m_nrc_no = fields.Char('Mother NRC')
    address = fields.Char('Address')
    mobile = fields.Char('Mobile Number')
    email = fields.Char('Email')

    def get_name(self):
        """To generate name for the model"""
        for i in self:
            i.name = str(i.student_id.name)
