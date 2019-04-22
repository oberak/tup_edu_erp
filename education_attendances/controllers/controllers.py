# -*- coding: utf-8 -*-
from odoo import http

# class Myproject(http.Controller):
#     @http.route('/myproject/myproject/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/myproject/myproject/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('myproject.listing', {
#             'root': '/myproject/myproject',
#             'objects': http.request.env['myproject.myproject'].search([]),
#         })

#     @http.route('/myproject/myproject/objects/<model("myproject.myproject"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('myproject.object', {
#             'object': obj
#         })