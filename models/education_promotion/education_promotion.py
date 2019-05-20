from datetime import datetime
from dateutil import relativedelta
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class EducationPromotion(models.Model):
    _inherit = 'education.promotion'    
    _description = 'Promotion'

    class_id = fields.Many2one('education.class.division', string='Class')

    # @api.onchange('name')
    # def onchange_class(self):
    #     for rec in self.env['education.class.division'].search([('academic_year_id', '=', self.name.id)]):
    #         self.class_id = rec.id       
    #         print(rec.id)
    #     return 
   
    def compute_final_result(self):
        self.state = 'result_computed'
        obj=self.env['education.exam'].search([('academic_year', '=', self.name.id),('division_id', '=', self.class_id.id)])
        for i in self.env['education.exam.results'].search([('exam_id', '=', obj.id)]):
            for student in i.division_id.students_details:
                student.unlink()
        for i in self.env['education.exam.results'].search([('exam_id', '=', obj.id)]):            
            if i.exam_id.exam_type.school_class_division_wise == 'final':
                    if i.overall_pass:
                        self.env['education.student.final.result'].create({
                            'student_id': i.student_id.id,
                            'final_result': 'pass',
                            'division_id': i.division_id.id,
                            'academic_year': i.division_id.academic_year_id.id,
                            'closing_id': self.id,
                        })
                    else:
                        self.env['education.student.final.result'].create({
                            'student_id': i.student_id.id,
                            'final_result': 'fail',
                            'division_id': i.division_id.id,
                            'academic_year': i.division_id.academic_year_id.id,
                            'closing_id': self.id,
                        })
    
    def close_academic_year(self):
        self.state = 'close'
        name = str(fields.Date.from_string(self.name.ay_end_date).year)+"-" + str(fields.Date.from_string(self.name.ay_end_date).year + 1) 
        new_academic_year = self.env['education.academic.year'].search([('name', '=',name)])       
        if not new_academic_year:
            new_academic_year = self.env['education.academic.year'].create(
                {
                    'name': str(fields.Date.from_string(self.name.ay_end_date).year)+"-" +
                            str(fields.Date.from_string(self.name.ay_end_date).year + 1),
                    'ay_start_date': self.name.ay_end_date,
                    'ay_end_date': str(fields.Date.from_string(self.name.ay_end_date) +
                                    relativedelta.relativedelta(months=+12))[:10],

                })
        obj=self.env['education.exam'].search([('academic_year', '=', self.name.id),('division_id', '=', self.class_id.id)])
        print('obj.division_id.id >>>>>>>>>',obj.division_id.id)
        obj2 = self.env['education.class.division'].search([('academic_year_id', '=', self.name.id),('id', '=', obj.division_id.id)])
        print('obj2 >>>>>>>>>>>>',obj2)
       # For the class is not last_class
        major_id = obj.class_id.major_id.id
        promote_batch = self.env['education.class'].create({
                    'ay_id':new_academic_year.id,
                    'major_id':major_id,
                    })
        class_id = promote_batch.id
        print('class id >>>>>>>>>>>',class_id)
        division_id = obj2.promote_division.id 
        print('division id >>>>>>>>>', division_id)       

        if division_id == 2:
            promote_division = 3
        elif division_id == 3:
            promote_division = 4
        elif division_id == 4:
            promote_division = 5
        elif division_id == 5:
            promote_division = 6
        else :
            promote_division = 7
           
        print('promote division >>>>>>>',promote_division)
        if obj2.is_last_class:
            self.env['education.class.division'].create({
                'name': obj2.name,
                'actual_strength': obj2.actual_strength,
                'academic_year_id': self.name.id,
                'class_id': obj2.is_last_class,
                'division_id': obj2.division_id.id,
                'is_last_class': obj2.class_id.id,
            })
        else:
            promote_class= self.env['education.class.division'].create({
                            'actual_strength': obj2.actual_strength,
                            'academic_year_id': new_academic_year.id,
                            'class_id': class_id,
                            'division_id': division_id,
                            'is_last_class': False,
                            'promote_division': promote_division,               
                        })
        print('>>>>>>>>>>>>>>>>')


        for j in self.env['education.class.division'].search([('academic_year_id', '=', self.name.id),('id', '=', obj.division_id.id)]):
            current_class = self.env['education.class.division'].search([
                                                    ('name', '=', j.name), ('academic_year_id', '=', j.academic_year_id.id)])
            print('current_class',current_class)
            if j.is_last_class:
                promotion_class = False
            else:
                promotion_class = self.env['education.class.division'].search([('name', '=', promote_class.name),
                                                                ('academic_year_id', '=', new_academic_year.id)])
            print('promotion_class',promotion_class)

            for k in j.students_details:
                if k.final_result == 'pass':
                    # add class history to student
                    self.env['education.class.history'].create({
                        'student_id':k.student_id.id,
                        'academic_year_id':promotion_class.academic_year_id.id,
                        'class_id': promotion_class.id,
                    })  
                    
                    k.student_id.class_id = promotion_class
                    print(k.student_id.id,'>>>>>>>> and ',k.student_id.class_id)                
                    self.env['education.student.final.result'].create({
                        'student_id': k.student_id.id,
                        'final_result': 'na',
                        'division_id':  promotion_class.id,
                        'academic_year': promotion_class.academic_year_id.id,

                    })

                elif k.final_result == 'fail':
                    k.student_id.class_id = current_class.id
                    self.env['education.student.final.result'].create({
                        'student_id': k.student_id.id,
                        'final_result': 'na',
                        'division_id': current_class.id,
                        'academic_year': current_class.academic_year_id.id,

                    })
        
       

    
    
   