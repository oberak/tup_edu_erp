from odoo import models, fields, api

class EducationExamResults(models.Model):
    _inherit = 'education.exam.results'

    division_id = fields.Many2one('education.class.division', string='Class')  # Rename Division to Class

    # add fields
    major_id = fields.Char(string="Major")                    
    pro_year = fields.Char(string='Program Year')

class ResultsSubjectLine(models.Model):
    _inherit = 'results.subject.line'

    division_id = fields.Many2one('education.class.division', string='Class') # Rename Division to Class

    
    
    

