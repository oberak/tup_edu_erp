from odoo import fields, models, api
from odoo.exceptions import ValidationError

class EmployeeCategory(models.Model):
    _inherit = 'hr.employee'
    _description = "Employee"
    

    #add field
    place_of_birth = fields.Char(string='Place Of Birth', required=True, help="Enter Place of Birth")
    certificate_level = fields.Char(String='Certificate Level', required=True, help="Enter certificate level")
    related_field = fields.Char(string='Related Field', required=False, help="Enter related field")
