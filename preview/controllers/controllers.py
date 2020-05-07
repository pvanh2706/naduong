# -*- coding: utf-8 -*-
from odoo import http

# class Preview(http.Controller):
#     @http.route('/preview/preview/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/preview/preview/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('preview.listing', {
#             'root': '/preview/preview',
#             'objects': http.request.env['preview.preview'].search([]),
#         })

#     @http.route('/preview/preview/objects/<model("preview.preview"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('preview.object', {
#             'object': obj
#         })