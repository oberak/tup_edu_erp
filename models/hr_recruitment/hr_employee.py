from odoo import fields, models, api
from odoo.exceptions import ValidationError

class EmployeeCategory(models.Model):
    _inherit = 'hr.employee'
    _description = "Employee"
    
    # get student list for subject teacher 
    @api.multi
    def get_class(self,values):
        class_list = []
        faculty_id= self.env['education.faculty'].search([('employee_id', '=', values)]).id
        for rec in self.env['education.timetable.schedule'].search([('faculty_id', '=', faculty_id)]):         
            class_id = rec.class_division.id
            class_list.append(class_id)
        class_list = list(dict.fromkeys(class_list))
        return class_list
       

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
    research_id = fields.Many2one('hr.paperpublication', string='Title Of Research Article', help="Enter Research Article")
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
    




class TupPaperPublicationRecord(models.Model):
    _name = 'hr.paperpublication'
    _description = 'Paper Publication Record'
    _inherit = ['mail.thread']

    #new fields
    title_of_research_article = fields.Char(string='Title Of Research Article', required=True, help="Enter Research Article")
    author_id = fields.Many2one('hr.employee', string='Author Name', required=True, help="Enter Author Name")
    rel_sub = fields.Char(string='Related Subject Specialization', required=True, help="Enter Related Subject Specification")
    publicated_date = fields.Date(
        'Publicated Date', required=True, default=lambda self: fields.Date.today(),
        track_visibility="onchange") 
    # vol_no = fields.Char(string='Vol No:', required=True, help="Enter Paper Volume Number")
    # page_range = fields.Integer(string='Page_range', required=True, help="Enter Page range")