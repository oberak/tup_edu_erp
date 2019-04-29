from odoo import fields, models, _, api
from odoo.exceptions import ValidationError

class AttendanceLine(models.Model):
    _name = 'attendances.line'
    _inherit = ['mail.thread']
    _rec_name = 'attendances_id'

    
    student_id = fields.Many2one(
        'education.student', 'Student', required=True, track_visibility="onchange")
    attendance_date = fields.Date(
        'Date', related='attendances_id.attendance_date', required=True, default=lambda self: fields.Date.today(),
        track_visibility="onchange")

    class_id = fields.Many2one('education.class', string="Batch")
    division_id = fields.Many2one('education.class.division', string='Class', required=True)
    student_list = fields.One2many('education.student.list', 'connect_id', string="Students")
    attendances_id = fields.Many2one(
        'attendances.sheet', 'Attendances Sheet', required=True,
        track_visibility="onchange", ondelete="cascade")
        
    # for assign student
    # present = fields.Boolean(
    #     'Present ?', default=True, track_visibility="onchange")
    # remark = fields.Char('Remark', track_visibility="onchange")
    
    # _sql_constraints = [
    #     ('unique_student',
    #      'unique(student_id,attendances_id,attendance_date)',
    #      'Student must be unique per Attendance.'),
    # ]
    
