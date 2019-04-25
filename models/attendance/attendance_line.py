from odoo import models, fields
from odoo.exceptions import ValidationError

class AttendanceLine(models.Model):
    _name = 'education.attendance.line'
    _inherit = ['mail.thread']
    _rec_name = 'attendance_id'

    attendance_id = fields.Many2one(
        'education.attendance.sheet', 'Attendance Sheet', required=True,
        track_visibility="onchange", ondelete="cascade")
    student_id = fields.Many2one(
        'education.student', 'Student', required=True, track_visibility="onchange")
    present = fields.Boolean(
        'Present ?', default=True, track_visibility="onchange")
    
    class_id = fields.Many2one(
        'education.class', 'Batch', store=True,
        readonly=True)
    division_id = fields.Many2one(
        'education.class.division', 'Class',
        related='attendance_id.register_id.division_id', store=True,
        readonly=True)
    remark = fields.Char('Remark', size=256, track_visibility="onchange")
    attendance_date = fields.Date(
        'Date', related='attendance_id.attendance_date', store=True,
        readonly=True, track_visibility="onchange")

    
