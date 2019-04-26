from odoo import models, fields, api
from odoo.exceptions import ValidationError

class AttendanceSheet(models.Model):
    _name = 'education.attendance.sheet'
    _inherit = ['mail.thread']

    @api.multi
    @api.depends('attendance_line.present')
    def _compute_total_present(self):
        for record in self:
            record.total_present = self.env['education.attendance.line'].search_count(
                [('present', '=', True), ('attendance_id', '=', record.id)])

    @api.multi
    @api.depends('attendance_line.present')
    def _compute_total_absent(self):
        for record in self:
            record.total_absent = self.env['education.attendance.line'].search_count(
                [('present', '=', False), ('attendance_id', '=', record.id)])

    name = fields.Char('Name', required=True, size=32)
        
    class_id = fields.Many2one(
        'education.class', store=True,
        readonly=True)
    division_id = fields.Many2one(
        'education.class.division', 'Class',  store=True,
        readonly=True)
    
    attendance_date = fields.Date(
        'Date', required=True, default=lambda self: fields.Date.today(),
        track_visibility="onchange")
    attendance_line = fields.One2many(
        'education.attendance.line', 'attendance_id', 'Attendance Line')
    total_present = fields.Integer(
        'Total Present', compute='_compute_total_present',
        track_visibility="onchange")
    total_absent = fields.Integer(
        'Total Absent', compute='_compute_total_absent',
        track_visibility="onchange")
    faculty_id = fields.Many2one('education.faculty', 'Faculty')

    
