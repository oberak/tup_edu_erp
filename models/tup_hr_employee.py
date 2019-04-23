from odoo import fields, models, api
from odoo.exceptions import ValidationError

class EmployeeCategory(models.Model):
    _inherit = 'hr.employee'
    _description = "Employee"
    

    
