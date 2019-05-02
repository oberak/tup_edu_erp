from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class EducationStudentsAttendance(models.Model):
    _name = 'education.attendances'

    name = fields.Char(compute='get_name', string='Attendance Sheet Name', default='New')
    # class_id = fields.Many2one('education.class', string='Class')
    division_id = fields.Many2one('education.class.division', string='Class', required=True)
    date = fields.Date(string='Date', default=fields.Date.today, required=True)
    attendance_line = fields.One2many('education.attendances.line', 'attendance_id', string='Attendance Line')
    attendance_created = fields.Boolean(string='Attendance Created')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], default='draft')
    academic_year = fields.Many2one('education.academic.year', string='Academic Year',
                                    related='division_id.academic_year_id', store=True)
    subject = fields.Many2one('education.subject', string='Subject', required=True)

    # Naming Class/Attendance_date
    def get_name(self):
        """To generate name for the model"""
        for i in self:
            i.name = str(i.division_id.name) + "/" + str(i.date)

    @api.model
    def create(self, vals):
        res = super(EducationStudentsAttendance, self).create(vals)
        res.class_id = res.division_id.class_id.id
        attendance_obj = self.env['education.attendances']
        already_created_attendance = attendance_obj.search(
            [('division_id', '=', res.division_id.id), ('date', '=', res.date) ])
        if len(already_created_attendance) > 1:
            raise ValidationError(
                _('Attendance register of %s is already created on "%s"', ) % (res.division_id.name, res.date))
        return res

    @api.multi
    def create_attendance_line(self):
        self.name = str(self.date)
        attendance_line_obj = self.env['education.attendances.line']
        students = self.division_id.student_ids
        if len(students) < 1:
            raise UserError(_('There are no students in this Class'))
        for student in students:
            data = {
                'name': self.name,
                'attendance_id': self.id,
                'student_id': student.id,
                'student_name': student.name,
                'class_id': self.division_id.class_id.id,
                'division_id': self.division_id.id,
                'date': self.date,
            }
            attendance_line_obj.create(data)
        self.attendance_created = True

    
    @api.multi
    def attendance_done(self):
        for records in self.attendance_line:
            records.state = 'done'
        self.state = 'done'

    @api.multi
    def set_to_draft(self):
        for records in self.attendance_line:
            records.state = 'draft'
        self.state = 'draft'


class EducationAttendanceLine(models.Model):
    _name = 'education.attendances.line'

    name = fields.Char(string='Name')
    attendance_id = fields.Many2one('education.attendances', string='Attendance Id')
    student_id = fields.Many2one('education.student', string='Student')
    student_name = fields.Char(string='Student', related='student_id.name', store=True)
    class_id = fields.Many2one('education.class', string='Batch', required=True)
    division_id = fields.Many2one('education.class.division', string='Class', required=True)
    date = fields.Date(string='Date', required=True)

# add periods
    one = fields.Boolean(string='Period one')
    two = fields.Boolean(string='Period two')
    three = fields.Boolean(string='Period three')
    four = fields.Boolean(string='Period four')
    five = fields.Boolean(string='Period five')
    six = fields.Boolean(string='Period six')
    
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], string='State', default='draft')
#     academic_year = fields.Many2one('education.academic.year', string='Academic Year',
#                                     related='division_id.academic_year_id', store=True)
