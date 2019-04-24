from odoo import fields, models, _, api
from odoo.exceptions import ValidationError

class EducationClass(models.Model):
    _inherit = 'education.class'

    #modify Fields name
    name = fields.Char(string='Batch', required=True, help="Enter the Name of the Batch")

class EducationDivision(models.Model):
    _inherit = 'education.division'

    #modify Fields name
    name = fields.Char(string='Program Year', required=True, help="Enter the Name of the Program Year")

class EducationClassDivision(models.Model):
    _inherit = 'education.class.division'

    #modify Fields name
    name = fields.Char(string='Class', readonly=True)
    class_id = fields.Many2one('education.class', string='Batch', required=True,
                               help="Select the Batch")
    division_id = fields.Many2one('education.division', string='Program Year', required=True,
                                  help="Select the Program Year")