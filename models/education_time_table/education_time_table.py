# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class EducationTimeTable(models.Model):
    _name = 'education.timetable'
    _inherit = 'education.timetable'
    _description = 'Timetable'
    color = fields.Integer()
    

    name = fields.Char(compute='get_name')
    period_id = fields.Many2one('timetable.period', string="Period", required=True,)
    time_from = fields.Float(string='From', required=True,
                             index=True, help="Start and End time of Period.")
    time_till = fields.Float(string='Till', required=True)
    
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

    state = fields.Selection([('draft', 'Draft'), 
                              ('confirm', 'Confirm'), ('done', 'Done')],
                             string='State', required=True, default='draft', track_visibility='onchange')

    # @api.multi
    # def unlink(self):
    #     """Return warning if the Record is in done state"""
    #     for rec in self:
    #         if rec.state == 'done':
    #             raise ValidationError(_("Cannot delete Record in Done state"))

    # @api.multi
    # def timetable_confirm(self):
    #     """Confirm the Timetable"""
    #     for rec in self:
    #         rec.write({
    #             'state': 'done'
    #         })


class EducationTimeTableSchedule(models.Model):
    _name = 'education.timetable.schedule'
    _inherit = 'education.timetable.schedule'
    _description = 'Timetable Schedule'
    _rec_name = 'period_id'
   
    
    hours = fields.Float(string='Hours', required=True)
    description = fields.Text(string='Syllabus Modules')
    classroom = fields.Char(string='Class Room')

    sub_type = fields.Selection([('is_language', 'Lecture'), ('is_tutorial', 'Tutorial'), ('is_lab', 'Practical')],
                            string='Type', default="is_language", required=True,
                            help="Choose the type of the subject")

   

   