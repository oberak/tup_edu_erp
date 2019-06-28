from odoo import fields, models, _, api
from odoo.exceptions import ValidationError

class EducationStudentClass(models.Model):
    _name='education.student.class'
    _inherit = 'education.student.class'
    
    class_id = fields.Many2one('education.class', string='Batch')

class EducationStudentList(models.Model):
    _inherit = 'education.student.list'

    connect_id = fields.Many2one('education.student.class', string='Batch')
    class_id = fields.Many2one('education.class', string='Batch')

class StudentAssignRollNo(models.Model):
    _name='education.student.class.division'

    class_division = fields.Many2one('education.class.division', string='Class')
    state = fields.Selection([('draft', 'Draft'), ('done', 'Confirm')], default='draft')
    student_ids = fields.One2many('students.rollno.list','list_id',string='Student Attendance Ids')

    @api.multi
    def assign_rollno(self):
        i=0
        for rec in self:
            s_ids = self.env['education.student'].search([('class_id','=',self.class_division.id)],order='total_marks desc')
            if s_ids:
                for s_id in s_ids:
                    i+=1
                    roll_no = str(s_id.class_id.division_id.name)+'-'+str(s_id.major_id.major_code)+'-'+str(i)
                    s_id.roll_no = roll_no
                    data={
                        'student_id': s_id.id,
                        'roll_no' : roll_no,
                        'list_id' : rec.id,
                    }
                    domain ={
                        'roll_no': s_id.roll_no,
                    }
                    self.env['education.student'].update(domain)
                    self.env['students.rollno.list'].create(data)
            rec.state ='done'
                

            

class StudentList(models.Model):
    _name='students.rollno.list'

    student_id = fields.Many2one('education.student', string='Student')
    roll_no = fields.Char('Roll No')
    list_id = fields.Many2one('education.student.class.division',string='Student Class')

    