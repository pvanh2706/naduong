# -*- coding: utf-8 -*-
from odoo import http

# class PreviewFile(http.Controller):
#     @http.route('/preview_file/preview_file/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/preview_file/preview_file/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('preview_file.listing', {
#             'root': '/preview_file/preview_file',
#             'objects': http.request.env['preview_file.preview_file'].search([]),
#         })

#     @http.route('/preview_file/preview_file/objects/<model("preview_file.preview_file"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('preview_file.object', {
#             'object': obj
#         })