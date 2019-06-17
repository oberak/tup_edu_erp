from datetime import datetime, date
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import calendar

class EducationSubjectAttendance(models.Model):
    _name = 'education.subject.attendances'

    name = fields.Char(compute='get_name',string='Monthly Attendance Name', default='New')
    class_division = fields.Many2one('education.class.division', string='Class', required=True, 
        domain=lambda self: [('academic_year_id', '=', self.env['education.academic.year']._get_current_ay().id)])
    student_id = fields.Many2one('education.student', string='Student')
    month = fields.Selection([('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'),
                          ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'), 
                          ('09', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December'), ], 
                          string='Month')
    subject_attendance = fields.Float('Attendance')
    total_s_attendances = fields.Float('Total Attendance')
    percent_s_attendance = fields.Float('Attendance (%) ')
    subject = fields.Many2one('education.subject', string='Subject', required=True)
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')],string='State', default='draft', track_visibility='onchange')
    d_att_ids = fields.One2many('education.attendances.line','sub_att_id',string='Daily Attendance Ids')
    m_att_id = fields.Many2one('education.monthly.attendances',string='Monthly Attendance')

    @api.onchange('class_division')
    def _onchange_class(self):
        students = self.class_division.student_ids 
        student_list = []       
        for stu in students:
            student_list.append(stu.id)
        for rec in self:
            obj = self.env['education.timetable.schedule'].search([('class_division', '=', rec.class_division.id)])
            subject_list = []
            if obj:
                for sub_id in obj:
                    subject_list.append(sub_id.subject.id)        
        vals = {
            'domain': {
                'student_id': [('id', 'in', student_list)],
                'subject': [('id', 'in', subject_list)],
            }
        }
        return vals

    def sub_attendance(self):
        month = False
        sub_atts= 0.0
        for rec in self:
            obj = self.env['education.attendances'].search([('class_division', '=', rec.class_division.id),('subject','=',rec.subject.id)])
            for attendance_id  in obj:
                for att_id in attendance_id:
                    daily_att = self.env['education.attendances.line'].search([('attendance_id','=',att_id.id)])
                    for d_att in daily_att:
                        month = datetime.strftime(datetime.strptime(d_att.date, "%Y-%m-%d"), "%m")
                        if month == rec.month:
                            att = self.env['education.attendances.line'].search([('id','=',d_att.id),('student_id','=',rec.student_id.id),('date','=',d_att.date),('state','=','done'),('remark','=',True)])
                            for datt in att:
                                sub_atts += datt.hours
                                datt.sub_att_id = self.id
                                daily_attendance = datt.sub_att_id
                                data ={
                                    'sub_att_id' : daily_attendance.id,
                                }
                                self.env['education.attendances.line'].update(data) 
            rec.subject_attendance = sub_atts
            rec.percent_s_attendance = rec.subject_attendance * 100 / rec.total_s_attendances
            rec.state = 'done'
    
    # Naming Class/Attendance_date
    def get_name(self):
        """To generate name for the model"""
        month_name= False
        for i in self:
            if i.month == '01':
                month_name ='January'
            elif i.month == '02':
                month_name = 'Feburary'
            elif i.month == '03':
                month_name = 'March'
            elif i.month == '04':
                month_name = 'Aprial'
            elif i.month == '05':
                month_name = 'May'
            elif i.month == '06':
                month_name = 'June'
            elif i.month == '07':
                month_name = 'July'
            elif i.month == '08':
                month_name = 'August'
            elif i.month == '09':
                month_name = 'September'
            elif i.month == '10':
                month_name = 'October'
            elif i.month == '11':
                month_name = 'November'
            elif i.month == '12':
                month_name = 'December'
            i.name = str(i.class_division.name)+ "/" + str(i.student_id.name)+"/" + str(i.subject.name)+ "/" +month_name+' Attendance'
    
    @api.model
    def create(self, vals):
        res = super(EducationSubjectAttendance, self).create(vals)        
        m_attendance = self.env['education.subject.attendances'].search(
            [('month', '=', res.month), ('student_id', '=', res.student_id.id),('subject', '=', res.subject.id) ])
        if len(m_attendance) > 1:
            raise ValidationError(
                _(' %s Attendance  of %s is already created on "%s"', ) % (res.subject.name,res.student_id.name, res.month))
        return res


class EducationMonthlyAttendance(models.Model):
    _name = 'education.monthly.attendances'

    name = fields.Char(compute='get_name', string='Monthly Attendance Name', default='New')
    class_division = fields.Many2one('education.class.division', string='Class', required=True, 
        domain=lambda self: [('academic_year_id', '=', self.env['education.academic.year']._get_current_ay().id)])
    student_id = fields.Many2one('education.student', string='Student')
    month = fields.Selection([('01', 'January'), ('02', 'February'), ('03', 'March'), ('04', 'April'),
                          ('05', 'May'), ('06', 'June'), ('07', 'July'), ('08', 'August'), 
                          ('09', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December'), ], 
                          string='Month')
    stu_m_attendances = fields.Float('Monthly Attendance')
    total_attendances= fields.Float('Attendance per Month', default = 1.0)
    m_attendances_percent = fields.Float('Monthly Attendance (%) ')
    ay_id = fields.Many2one('education.academic.year',string='Academic Year',default=lambda self: self.env['education.academic.year']._get_current_ay())
    oatt_id = fields.Many2one('education.overall.attendances',string='Overall Attendance ID')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')],string='State', default='draft', track_visibility='onchange')
    sub_att_ids = fields.One2many('education.subject.attendances','m_att_id',string='Attendance by subject')

    @api.onchange('class_division')
    def _onchange_class(self):
        students = self.class_division.student_ids 
        student_list = []       
        for stu in students:
            student_list.append(stu.id)
        vals = {
            'domain': {
                'student_id': [('id', 'in', student_list)]
            }
        }
        return vals
  
    def monthly_attendance(self):
        m_att = 0.0
        for rec in self:
            obj = self.env['education.subject.attendances'].search([('student_id','=',rec.student_id.id),('class_division','=',rec.class_division.id),('month','=',rec.month)])
            for dat in obj:
                m_att += dat.subject_attendance
                dat.m_att_id = self.id
                data ={
                    'm_att_id' : dat.m_att_id.id,
                }
                self.env['education.monthly.attendances'].update(data)
            rec.stu_m_attendances = m_att
            rec.m_attendances_percent= rec.stu_m_attendances * 100 / rec.total_attendances
            rec.state='done'

    # Naming Class/Attendance_date
    def get_name(self):
        """To generate name for the model"""
        for i in self:
            if i.month == '01':
                month_name ='January'
            elif i.month == '02':
                month_name = 'Feburary'
            elif i.month == '03':
                month_name = 'March'
            elif i.month == '04':
                month_name = 'Aprial'
            elif i.month == '05':
                month_name = 'May'
            elif i.month == '06':
                month_name = 'June'
            elif i.month == '07':
                month_name = 'July'
            elif i.month == '08':
                month_name = 'August'
            elif i.month == '09':
                month_name = 'September'
            elif i.month == '10':
                month_name = 'October'
            elif i.month == '11':
                month_name = 'November'
            elif i.month == '12':
                month_name = 'December'
            i.name = str(i.class_division.name)+ "/" + str(i.student_id.name)+ "/" +month_name+' Attendance'
    
          
    @api.model
    def create(self, vals):
        res = super(EducationMonthlyAttendance, self).create(vals)        
        m_attendance = self.env['education.monthly.attendances'].search(
            [('month', '=', res.month), ('student_id', '=', res.student_id.id) ])
        if len(m_attendance) > 1:
            raise ValidationError(
                _('Monthly Attendance  of %s is already created on "%s"', ) % (res.student_id.name, res.month))
        return res
         
class EducationStudentsOverallAttendance(models.Model):
    _name = 'education.overall.attendances'

    ay_id = fields.Many2one('education.academic.year',string='Academic Year',default=lambda self: self.env['education.academic.year']._get_current_ay())
    name = fields.Char(compute='get_name', string='Overall Attendance', default='New')
    class_division = fields.Many2one('education.class.division', string='Class', required=True, 
        domain=lambda self: [('academic_year_id', '=', self.env['education.academic.year']._get_current_ay().id)])
    student_id = fields.Many2one('education.student', string='Student')
    total_attendances= fields.Float('Attendance per Academic Year')
    stu_overall_percent = fields.Float('Overall Attendance (%)')    
    stu_overall_attendances = fields.Float('Overall Attendance')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Done')],string='State', default='draft', track_visibility='onchange')
    matt_ids = fields.One2many('education.monthly.attendances','oatt_id',string='Monthly Attendance Ids')

    @api.onchange('class_division')
    def _onchange_class(self):
        students = self.class_division.student_ids 
        student_list = []       
        for stu in students:
            student_list.append(stu.id)
        vals = {
            'domain': {
                'student_id': [('id', 'in', student_list)]
            }
        }
        return vals

     # Naming Class/Attendance_date
    def get_name(self):
        """To generate name for the model"""
        for i in self:
            i.name = str(i.class_division.name)+ "/" + str(i.student_id.name)+ "/ Overall Attendances" 

    def overall_attendance(self):
        this_ay = self.env['education.academic.year']._get_current_ay()      
        overall_att = 0.0        
        for rec in self:    
            obj = self.env['education.monthly.attendances'].search([('student_id','=',rec.student_id.id),('class_division','=',self.class_division.id),('ay_id','=',this_ay.id)])
            if obj :
                for m_att in obj:                    
                    overall_att += m_att.stu_m_attendances
                    m_att.oatt_id = self.id
                    oatt = m_att.oatt_id
                    data ={
                        'oatt_id' : oatt.id,
                    }
                    self.env['education.monthly.attendances'].update(data)                    
            rec.stu_overall_attendances= overall_att        
            rec.stu_overall_percent = rec.stu_overall_attendances * 100 / rec.total_attendances
            rec.state = 'done' 
            

    @api.model
    def create(self, vals):
        res = super(EducationStudentsOverallAttendance, self).create(vals)        
        m_attendance = self.env['education.overall.attendances'].search(
            [('class_division', '=', res.class_division.id), ('student_id', '=', res.student_id.id) ])
        if len(m_attendance) > 1:
            raise ValidationError(
                _('Overall Attendance  of %s is already created on "%s"', ) % (res.student_id.name, res.class_division.name))
        return res       
        
