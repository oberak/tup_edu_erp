from odoo import fields, models, api
from odoo.exceptions import ValidationError

class EmployeeCategory(models.Model):
    _inherit = 'hr.employee'
    _description = "Employee"
    
    # get student list for subject teacher 
    @api.multi
    def get_class(self,values):
        class_list = []
        faculty_id= self.env['education.faculty'].search([('employee_id','=', values)]).id
        obj = self.env['education.faculty.classes'].search([('faculty_id', '=', faculty_id)])        
        for rec in obj:         
            c_id = rec.class_id.id
            class_list.append(c_id)
        class_list = list(dict.fromkeys(class_list))
        return class_list

    #modify fields
    parent_id = fields.Many2one('hr.employee', 'Head of Department')
    country_id = fields.Many2one(
        'res.country', 'Nationality', groups="hr.group_hr_user",default=145)

    #add field
    job_position = fields.Many2one('tup.job', string='Position')
    degree = fields.Selection([
            ('Ph.D', 'Ph.D'),
            ('ME', 'ME'),
            ('MCSc', 'MCSc'), 
            ('MSc', 'MSc'),
            ('MA', 'MA'),
            ('BE', 'BE'), 
            ('DCSc', 'DCSc'),
            ('BSc', 'BSc'),
            ('BA', 'BA'),
            ('B-Tech', 'B-Tech'),
            ('A.G.T.I', 'A.G.T.I'),
            ('Tutor', 'Tutor'),
            ('Demostrator', 'Demostrator'), ], 
             string='Degree')

    ## private infomation
    place_of_birth = fields.Char(string='Place Of Birth', required=True, help="Enter Place of Birth")   
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

    #education history
    edu_ids = fields.One2many('education.place.history', 'emp_id', string="Education History")
    #Job history
    job_ids = fields.One2many('education.job.history', 'emp_id', string="Job History")
    #abroad experience
    abroad_ids = fields.One2many('education.abroad.experience', 'emp_id', string="Abroad Experience")
    #relationship
    relation_ids = fields.One2many('employee.relationship', 'emp_id', string="Relationship")
    #relationship
    paper_ids = fields.One2many('education.research', 'emp_id', string="Research Record")

class ResearchRecord(models.Model):
    _name = 'education.research'
    _description = 'Research Record'
    _inherit = ['mail.thread']

    #new fields
    title = fields.Char(string='Title Of Research',help="Enter Research Article")
    name = fields.Char(string="Paper/Journal Name")
    specialization = fields.Char(string='Specialization', help="Enter Related Subject Specialization")
    pub_date = fields.Date(
        'Publication Date',  default=lambda self: fields.Date.today(),
        track_visibility="onchange") 
    paper_type = fields.Selection([
        ('paper', 'Paper'),
        ('journal', 'Journal'),
    ], string='Type', default='paper')
    vol_no = fields.Char(string='Vol No:', help="Enter Paper Volume Number")
    page_range = fields.Char(string='Page_range',  help="Enter Page range")
    emp_id = fields.Many2one('hr.employee', string='Author Name',  help="Enter Author Name")


class Job(models.Model):
    _name= 'tup.job'
    _description = 'Job Position'

    name =fields.Char('Job Position Name')
    salary = fields.Char('Salary')
    pay_scale = fields.Char('Pay Scale')

class EducationHistory(models.Model):
    _name= 'education.place.history'
    _description = 'Education Place History'

    edu_place = fields.Char('School/College/University/Training/Workshop')
    start_date = fields.Date(string='Start date',  help='Starting date of Education')
    end_date = fields.Date(string='End date',  help='Ending of Education')
    city = fields.Char(String='City' , help='City where is studied')
    rank = fields.Char('Education Level')
    emp_id = fields.Many2one('hr.employee', string='Employee')

class JobHistory(models.Model):
    _name= 'education.job.history'
    _description = 'Education Job History'

    job_place = fields.Char('Collage/University')
    start_date = fields.Date(string='Start date',  help='Starting date of Education')
    end_date = fields.Date(string='End date',  help='Ending of Education')
    position = fields.Many2one('tup.job', string='Job Position')
    emp_id = fields.Many2one('hr.employee', string='Employee')

class AbroadHistory(models.Model):
    _name= 'education.abroad.experience'
    _description = 'Education Abroad Experience'

    country = fields.Many2one('res.country', 'Country Name')
    start_date = fields.Date(string='Start date',  help='Starting date of Education')
    end_date = fields.Date(string='End date',  help='Ending of Education')
    reason = fields.Char('Description')
    withdraw_money = fields.Integer('Amount Money that had been withdrawn')
    emp_id = fields.Many2one('hr.employee', string='Employee')

class Relationship(models.Model):
    _name= 'employee.relationship'
    _description = 'Relationship'

    name = fields.Char('Name')
    nationality = fields.Many2one('res.country', 'Nationality', default=145)
    relation = fields.Char('Relation')
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
                            string='Gender',  default='male', track_visibility='onchange')
    occupation = fields.Char('Occupation')
    address = fields.Char('Address')
    emp_id = fields.Many2one('hr.employee', string='Employee')