from odoo import fields, models, api
from odoo.exceptions import ValidationError


class TupEducationFaculty(models.Model):
    _name = 'education.faculty'
    _inherit = 'education.faculty'
    _description = 'Faculty Record'


    # add fields
    nrc_no = fields.Char(string='NRC Number', required=True, help="Enter NRC Number of Student")