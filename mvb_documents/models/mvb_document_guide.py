from odoo import api, fields, models

class MVBDocumentGuide(models.Model):
    _name = 'mvb.document.guide'
    _description = 'Model hướng dẫn sử dụng tài liệu'

    name = fields.Char('')