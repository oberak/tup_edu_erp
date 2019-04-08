from odoo import fields, models, api
from odoo.exceptions import ValidationError

<<<<<<< HEAD
=======

>>>>>>> 66ee83ec6c82aed4ebb81124f2c7d929c3b47e15
class TupEducationFaculty(models.Model):
    _name = 'education.faculty'
    _inherit = 'education.faculty'
    _description = 'Faculty Record'

<<<<<<< HEAD
    #add field
    nrc_no = fields.Char(string='NRC Number', required=True, help="Enter NRC Number of Faculty")
=======

    # add fields
    nrc_no = fields.Char(string='NRC Number', required=True, help="Enter NRC Number of Student")
>>>>>>> 66ee83ec6c82aed4ebb81124f2c7d929c3b47e15
