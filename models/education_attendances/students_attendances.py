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
    #week_day = fields.Date(string='Week Day', default=datetime.today().strftime("%A"))
    week_day = fields.Char('Week Day')
    subject = fields.Many2one('education.subject', string='Subject', required=True)
    # application_id = fields.Many2one('education.application', string='Application No',
                                    #  domain="[('state', 'in', ['draft', 'verification', 'fee'])]")

    @api.onchange('class_division', 'date')
    def _onchange_class(self):
        # find timetable using class & semester
        selected = fields.Datetime.from_string(self.date)
        self.week_day = calendar.day_name[selected.weekday()]
        wod = self.week_day[0:3].lower()
        this_semester = self.env['education.semester']._get_current_semester()
        for record in self:
            if this_semester and record.class_division:
                timetable = self.env['education.timetable'].search([('semester', '=', this_semester.id), ('class_division', '=', record.class_division.id)])
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
            [('class_division', '=', res.class_division.id), ('date', '=', res.date) ,('subject','=',res.subject.id)])
        if len(already_created_attendance) > 1:
            raise ValidationError(
                _('Attendance register of %s and %s is already created on "%s"', ) % (res.class_division.name,res.subject.id, res.date))
        return res

    @api.multi
    def create_attendance_line(self): 
        wday = self.week_day
        this_semester = self.env['education.semester']._get_current_semester()
        for record in self:
            if this_semester and record.class_division:
                timetable = self.env['education.timetable'].search([('semester', '=', this_semester.id), ('class_division', '=', record.class_division.id)])

        if wday == 'Monday' :
            week_day = '0'
        elif wday == 'Tuesday' :
            week_day = '1'
        elif wday == 'Wednesday' :
            week_day = '2'
        elif wday == 'Thursday' :
            week_day = '3'
        elif wday == 'Friday' :
            week_day = '4'
        elif wday == 'Saturday' :
            week_day = '5'
        else :
            week_day ='6'

        schedule = self.env['education.timetable.schedule'].search([('timetable_id','=',timetable.id),('week_day','=',week_day),('subject','=',self.subject.id)])            
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
                'period' : schedule.period_id.id,
                'hours':schedule.hours,
                'class_division': self.class_division.id,
                'date': self.date,
            }
            attendance_line_obj.sudo().create(data)        
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
    class_division = fields.Many2one('education.class.division', string='Class')
    date = fields.Date(string='Date')   
    # add periods
    period= fields.Many2one('timetable.period', string="Period")
    hours = fields.Float('Durition')
    remark = fields.Boolean(string='Present')
    sub_att_id = fields.Many2one('education.subject.attendances',string='Monlhly Attendance ID')

    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')], string='State', default='draft')
#     academic_year = fields.Many2one('education.academic.year', string='Academic Year',
#                                     related='class_division.academic_year_id', store=True)
