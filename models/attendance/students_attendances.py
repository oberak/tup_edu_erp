from datetime import datetime, date
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import calendar

class EducationStudentsAttendance(models.Model):
    _name = 'education.attendances'

    name = fields.Char(compute='get_name', string='Attendance Sheet Name', default='New')
    # class_id = fields.Many2one('education.class', string='Class')
    class_division = fields.Many2one('education.class.division', string='Class', required=True, 
        domain=lambda self: [('academic_year_id', '=', self.env['education.academic.year']._get_current_ay().id)])
    date = fields.Date(string='Date', default=fields.Date.today, required=True)
    attendance_line = fields.One2many('education.attendances.line', 'attendance_id', string='Attendance Line')
    attendance_created = fields.Boolean(string='Attendance Created')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], default='draft')
    academic_year = fields.Many2one('education.academic.year', string='Academic Year',
                                    related='class_division.academic_year_id', store=True)
    
    # add fields to relate timetable
    week_day = fields.Char('Week Day')
    subject = fields.Many2one('education.subject', string='Subject', required=True)


    # application_id = fields.Many2one('education.application', string='Application No',
                                    #  domain="[('state', 'in', ['draft', 'verification', 'fee'])]")

    @api.onchange('class_division', 'date')
    def _onchange_class(self):
        # find timetable using class & semester
        this_semester = self.env['education.semester']._get_current_semester()
        wod = self.week_day[0:3].lower()
        print(this_semester, this_semester.id,  wod)
        
        if this_semester:
            timetable = self.env['education.timetable'].search([('semester', '=', this_semester.id)])
            subject_list = []
            if timetable:
                for tt_s in eval('timetable.timetable_'+wod):
                    subject_list.append(tt_s.subject.id)
            vals = {
                'domain': {
                    'subject': [('id', 'in', subject_list)]
                }
            }
            return vals

    # get_week day from date
    @api.onchange('date')
    def _get_day_of_date(self):
        for r in self:
            if r.date:
                selected = fields.Datetime.from_string(r.date)
                r.week_day = calendar.day_name[selected.weekday()]


    # Naming Class/Attendance_date
    def get_name(self):
        """To generate name for the model"""
        for i in self:
            i.name = str(i.class_division.name) + "/" + str(i.date)

    @api.model
    def create(self, vals):
        res = super(EducationStudentsAttendance, self).create(vals)
        res.class_id = res.class_division.class_id.id
        attendance_obj = self.env['education.attendances']
        already_created_attendance = attendance_obj.search(
            [('class_division', '=', res.class_division.id), ('date', '=', res.date) ])
        if len(already_created_attendance) > 1:
            raise ValidationError(
                _('Attendance register of %s is already created on "%s"', ) % (res.class_division.name, res.date))
        return res

    @api.multi
    def create_attendance_line(self):
        self.name = str(self.date)
        attendance_line_obj = self.env['education.attendances.line']
        students = self.class_division.student_ids
        if len(students) < 1:
            raise UserError(_('There are no students in this Class'))
        for student in students:
            data = {
                'name': self.name,
                'attendance_id': self.id,
                'student_id': student.id,
                'student_name': student.name,
                'class_id': self.class_division.class_id.id,
                'class_division': self.class_division.id,
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
    class_division = fields.Many2one('education.class.division', string='Class', required=True)
    date = fields.Date(string='Date', required=True)

# add periods
    one = fields.Boolean(string='1st')
    two = fields.Boolean(string='2nd')
    three = fields.Boolean(string='3rd')
    four = fields.Boolean(string='4th')
    five = fields.Boolean(string='5th')
    six = fields.Boolean(string='6th')
    remark = fields.Char(string='Remark')


    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], string='State', default='draft')
#     academic_year = fields.Many2one('education.academic.year', string='Academic Year',
#                                     related='class_division.academic_year_id', store=True)
