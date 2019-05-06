# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class EducationAcademic(models.Model):
    _inherit = 'education.academic.year'

    #modify fields
    sequence = fields.Integer(string='Sequence', required=False)
    ay_code = fields.Char(string='Code', required=False, help='Code of academic year', readonly=True)
    active = fields.Boolean(string='Active', default=True)

    @api.model
    def _get_current_ay(self):
        domain = [
            ('ay_start_date', '<=', datetime.now().strftime('%Y-%m-%d')),
            ('ay_end_date', '>=', datetime.now().strftime('%Y-%m-%d')),
        ]
        return self.search(domain, limit=1)

    # override for code
    @api.model
    def create(self, vals):
        """Return the code as a left four digit of Application Year"""        
        vals['ay_code'] = vals['name'][:4]
        return super(EducationAcademic, self).create(vals)

    #override for code
    @api.one
    @api.depends('name')
    def write(self, vals):
        if 'name' in vals:
            vals['ay_code'] = vals['name'][:4]
        vals['ay_code'] = vals['ay_code']
        return super(EducationAcademic, self).write(vals)
