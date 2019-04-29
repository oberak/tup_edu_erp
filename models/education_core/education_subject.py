# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class EducationSubject(models.Model):
    _inherit = 'education.subject'
    
    major_id = fields.Many2one('hr.department', string="Major",
                            required=True, domain=[('is_major', '=', True)],
                            help="Choose Major")
    is_tutorial = fields.Boolean(string='Tutorial', help="Tick if this is the Tutorial")
    is_class_work = fields.Boolean(string="Class Work", help="Tick if this is the class Work")

    # check logged user's department
    user_subjects=fields.Char(compute="_compute_user_subjects",search='user_subjects_search')
    
    @api.one
    @api.depends('major_id')
    def _compute_user_subjects(self):
        print('View my departemnt subjects')

    def user_subjects_search(self, operator, operand):
        employee_ids = self.env['hr.employee'].search([('user_id','in',self.env.user.login)]).ids
        return [('major_id.member_ids','in',employee_ids)]