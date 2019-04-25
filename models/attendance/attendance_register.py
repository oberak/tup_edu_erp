from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AttendanceRegister(models.Model):
    _name = 'education.attendance.register'
    _inherit = ['mail.thread']

    name = fields.Char(
        'Register Name', size=32, required=True, track_visibility='onchange')
    code = fields.Char(
        'Code', size=16, required=True, track_visibility='onchange')
    
    class_id = fields.Many2one(
        'education.class', 'Batch', required=True, track_visibility='onchange')
    division_id = fields.Many2one(
        'education.class.division', 'Class', required=True, track_visibility='onchange')
    subject_id = fields.Many2one(
        'education.subject', 'Subject', track_visibility='onchange')

    

    @api.onchange('class_id')
    def onchange_class(self):
        self.division_id = False
