# -*- coding: utf-8 -*-
from odoo import http

# class Tup-edu-erp(http.Controller):
#     @http.route('/tup-edu-erp/tup-edu-erp/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/tup-edu-erp/tup-edu-erp/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('tup-edu-erp.listing', {
#             'root': '/tup-edu-erp/tup-edu-erp',
#             'objects': http.request.env['tup-edu-erp.tup-edu-erp'].search([]),
#         })

#     @http.route('/tup-edu-erp/tup-edu-erp/objects/<model("tup-edu-erp.tup-edu-erp"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('tup-edu-erp.object', {
#             'object': obj
#         })