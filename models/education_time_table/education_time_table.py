# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

class EducationTimeTable(models.Model):
    _inherit = 'education.timetable'

    # to modify the name (get_name) 
    name = fields.Char(compute='get_name') 
        
    # add fields
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'Done')],
                             default='draft')
    semester = fields.Many2one('education.semester', string="Semester")                       
    major_id = fields.Many2one('hr.department','Major')
    timetable_thu = fields.One2many('education.timetable.schedule', 'timetable_id',
                                     domain=[('week_day', '=', '3')])                      

    def get_name(self):
        """To generate name for the model"""
        for i in self:
            i.name = str(i.class_division.name) + "(" + str(i.semester.name) +")"

  
    @api.onchange('class_division')
    @api.constrains('class_division')
    def onchange_class_division(self):
        """Gets the major_id"""
        for i in self:
            i.academic_year = i.class_division.academic_year_id
            obj = self.env['education.class.division'].search([('id','=',i.class_division.id)])
            obj2 = self.env['education.class'].search([('id','=',obj.class_id.id)])
            i.major_id =obj2.major_id.id
        return

    @api.onchange('academic_year')
    def onchange_academic_year(self):
        """Gets the Semesters"""
        for record in self:
            obj = self.env['education.semester'].search([('academic_year', '=', record.academic_year.id)])            
            sem_list = []
            if obj :
                for sem_id in obj:                   
                    sem_list.append(sem_id.id)           
            vals = {
                'domain': {
                    'semester': [('id', 'in', sem_list)]
                }
            }
            return vals 
 
    @api.onchange('period_id')
    def onchange_period_id(self):
        """Gets the start and end time of the period"""
        for i in self:
            i.time_from = i.period_id.time_from
            i.time_till = i.period_id.time_to

    @api.multi
    def close_timetable(self):
        self.state = 'done'
    
    @api.multi
    def confirm_timetable(self):
        if len(self.timetable_mon) + len(self.timetable_tue) + len(self.timetable_wed) + len(self.timetable_thur) + len(self.timetable_fri) + len(self.timetable_sat) + len(self.timetable_sun)  < 1:
            raise UserError(_('Please Add Subject schedule'))
        self.state = 'confirm' 
    
    @api.model
    def create(self, vals):
        res = super(EducationTimeTable, self).create(vals)        
        timetable = self.env['education.timetable'].search(
            [('class_division', '=', res.class_division.id), ('semester', '=', res.semester.id) ])
        if len(timetable) > 1:
            raise ValidationError(
                _('Timetable  of %s is already created on "%s"', ) % (res.class_division.name, res.semester.name))
        return res
        
class EducationTimeTableSchedule(models.Model):
    _inherit = 'education.timetable.schedule'
    _rec_name = 'period_id'
   
    # modify field name
    period_id = fields.Many2one('timetable.period', string="Period (from)", required=True)
      
    # add fields
    period_id_to= fields.Many2one('timetable.period', string="Period (to)", required=True)  
    hours = fields.Float(string='Hours', required=True)
    description = fields.Text(string='Syllabus Modules')
    classroom = fields.Char(string='Class Room')
    sub_type = fields.Selection([('is_language', 'Lecture'), ('is_tutorial', 'Tutorial'), ('is_lab', 'Practical')],
                            string='Type', default="is_language", required=True,
                            help="Choose the type of the subject")
