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

    def get_name(self):
        """To generate name for the model"""
        for i in self:
            i.name = str(i.class_division.name) + "/" + str(i.academic_year.name)

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

class EducationTimeTableSchedule(models.Model):
    _inherit = 'education.timetable.schedule'
    _rec_name = 'period_id'
   
    hours = fields.Float(string='Hours', required=True)
    description = fields.Text(string='Syllabus Modules')
    classroom = fields.Char(string='Class Room')
    sub_type = fields.Selection([('is_language', 'Lecture'), ('is_tutorial', 'Tutorial'), ('is_lab', 'Practical')],
                            string='Type', default="is_language", required=True,
                            help="Choose the type of the subject")

