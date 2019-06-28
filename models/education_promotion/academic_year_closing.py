from odoo import fields, models, _, api
from odoo.exceptions import ValidationError

class AcademicYearClosing(models.Model):
    _inherit = 'education.class.division'

    promote_class = fields.Many2one('education.class', string='Promotion Batch')
    promote_division = fields.Many2one('education.division', string='Promotion Program Year')

class EducationStudentFinalResult(models.Model):
    _inherit = 'education.student.final.result'

    #add field
    total_marks= fields.Integer('Total Marks')