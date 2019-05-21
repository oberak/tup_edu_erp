from odoo import fields, models, api
from odoo.exceptions import ValidationError

class User(models.Model):

    _inherit = 'res.users'

    # get Class for the login student 
    @api.multi
    def get_class(self,values):
        print(values,'>>>>>>>>>>>>>>>')
        obj= self.env['education.student'].search([('email', '=', values)])
        class_id= obj.class_id.id
        return class_id