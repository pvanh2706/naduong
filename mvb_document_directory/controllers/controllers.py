# -*- coding: utf-8 -*-
from odoo import http

# class MvbDocumentDirectory(http.Controller):
#     @http.route('/mvb_document_directory/mvb_document_directory/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mvb_document_directory/mvb_document_directory/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mvb_document_directory.listing', {
#             'root': '/mvb_document_directory/mvb_document_directory',
#             'objects': http.request.env['mvb_document_directory.mvb_document_directory'].search([]),
#         })

#     @http.route('/mvb_document_directory/mvb_document_directory/objects/<model("mvb_document_directory.mvb_document_directory"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mvb_document_directory.object', {
#             'object': obj
#         })