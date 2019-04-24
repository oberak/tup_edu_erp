from odoo import fields, models, _, api
from odoo.exceptions import ValidationError

class EducationStudentClass(models.Model):
    _name='education.student.class'
    _inherit = 'education.student.class'
    
    class_id = fields.Many2one('education.class', string='Batch')

class EducationStudentList(models.Model):
    _inherit = 'education.student.list'

    connect_id = fields.Many2one('education.student.class', string='Batch')
    class_id = fields.Many2one('education.class', string='Batch')

    