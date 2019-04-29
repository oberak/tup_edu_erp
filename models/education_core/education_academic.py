# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class EducationAcademic(models.Model):
    _inherit = 'education.academic.year'

    @api.model
    def _get_current_ay(self):
        domain = [
            ('ay_start_date', '<=', datetime.now().strftime('%Y-%m-%d')),
            ('ay_end_date', '>=', datetime.now().strftime('%Y-%m-%d')),
        ]
        return self.search(domain, limit=1)
