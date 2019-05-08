from dateutil import relativedelta
from odoo import models, fields, api, _


class EducationPromotion(models.Model):
    _name = 'education.promotion'
    _inherit = ['education.promotion']
    
    _description = 'Promotion'

    class_id = fields.Many2one('education.class.division', string="Class")
    academic_year_id = fields.Many2one('education.academic.year', string='Academic Year', required=True, 
                            default=lambda self: self.env['education.academic.year']._get_current_ay(),
                            help="Select the Academic Year")
    class_history_ids = fields.One2many('education.class.history', 'student_id', string="Application No")