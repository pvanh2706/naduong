# -*- coding: utf-8 -*-
from odoo import http

# class GMail(http.Controller):
#     @http.route('/g_mail/g_mail/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/g_mail/g_mail/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('g_mail.listing', {
#             'root': '/g_mail/g_mail',
#             'objects': http.request.env['g_mail.g_mail'].search([]),
#         })

#     @http.route('/g_mail/g_mail/objects/<model("g_mail.g_mail"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('g_mail.object', {
#             'object': obj
#         })