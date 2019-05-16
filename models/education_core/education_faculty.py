from odoo import fields, models, api
from odoo.exceptions import ValidationError

class EducationFaculty(models.Model):
    _name = 'education.faculty'
    _inherit = 'education.faculty'
    _description = 'Faculty Record'

    # modify name value in create employee 
    @api.multi
    def create_employee(self):
        """Creating the employee for the faculty"""
        for rec in self:
            values = {
                'name': rec.name,
                'gender': rec.gender,
                'birthday': rec.date_of_birth,
                'image': rec.image,
                'work_phone': rec.phone,
                'work_mobile': rec.mobile,
                'work_email': rec.email,
            }
            emp_id = self.env['hr.employee'].create(values)
            rec.employee_id = emp_id.id

    #add field
    nrc_no = fields.Char(string='NRC Number', required=True, help="Enter NRC Number of Faculty")
