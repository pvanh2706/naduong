# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class DocumentGuide(models.TransientModel):
    _name = 'document.guide'
    _description = 'Tài liệu hướng dẫn sử dụng phần mền Quản lý Lịch công tác tuần'

    def name(self):
        res = 'Tài liệu hướng dẫn'
        return res
    name = fields.Char(string="", required=False, default=name)


