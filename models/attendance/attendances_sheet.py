from odoo import fields, models, _, api
from odoo.exceptions import ValidationError

class AttendanceSheet(models.Model):
    _name = 'attendances.sheet'
    _inherit = ['mail.thread']
    

    name = fields.Char(compute='get_name')
    class_id = fields.Many2one('education.class', string="Batch")
    division_id = fields.Many2one('education.class.division', string='Class', required=True)
    attendance_date = fields.Date(
        'Date', required=True, default=lambda self: fields.Date.today(),
        track_visibility="onchange")
    student_id = fields.Many2one(
        'education.student', 'Student', required=True, track_visibility="onchange")
    student_list = fields.One2many('education.student.list', 'connect_id', string="Students")
    attendances_line = fields.One2many(
        'attendances.line', 'attendances_id', 'Attendances Line')
    
    # state = fields.Selection([('draft', 'Draft'), ('done', 'Done')],
    #                          string='State', required=True, default='draft', track_visibility='onchange')
    

    # Naming Class/Attendance_date
    def get_name(self):
        """To generate name for the model"""
        for i in self:
            i.name = str(i.division_id.name) + "/" + str(i.attendance_date)


