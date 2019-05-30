import datetime
from odoo import fields, models, api, _
from datetime import date


class EducationDocuments(models.Model):
    _inherit = 'education.documents'
    _description = "Student Documents"
    

    #Modify fields
    reference = fields.Char(string='Document Name', required=True, copy=False)
   