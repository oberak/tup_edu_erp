from odoo import fields, models, api
from odoo.exceptions import ValidationError

class EmployeeCategory(models.Model):
    _inherit = 'hr.employee'
    _description = "Employee"
    

    #add field
    place_of_birth = fields.Char(string='Place Of Birth', required=True, help="Enter Place of Birth")
    certificate_level = fields.Char(String='Certificate Level', required=True, help="Enter certificate level")
    related_field = fields.Char(string='Related Field', required=False, help="Enter related field")
    graduated_university = fields.Char(string= 'Graduated University', required=True, help="Enter graduated university")
    height = fields.Char(string='Height', help="Enter height")
    hair_color = fields.Char(string='Hair Color', help="Enter hair color")
    eye_color = fields.Char(string='Eye Color', help="Enter eye color")
    noticeable = fields.Char(string='Noticeable Remark', help="Enter height")
    complexion = fields.Char(string='Complexion', help="Enter complexion")
    weight = fields.Char(string='weight', help="Enter weight")
    emergency_contact = fields.Char(string='Emergency Contact', required=True, help='Enter emergency contact')
    have_child = fields.Boolean(string="Have Children", default=False,
                                     help="If you have children")
    number_of_children = fields.Selection([
        ('one', 'One'),
        ('two', 'Two'),
        ('three', 'Three'),
        ('four', 'Four'),
        ('five', 'Five'),
        ('above five', 'Above Five')
    ], string='Number of Children', default='one')