# -*- coding: utf-8 -*-

from odoo import models, fields, api

class preview_file(models.Model):
    _name = 'preview_file.preview_file'

    name = fields.Char()
    attachment_ids = fields.Binary(string="Attachment")
    store_fname = fields.Char(string="File Name")

    # @api.model
    # def read(self, vals, vals1='', vals2='', val3=''):
    #     print("read --------------------", vals)
    #     print("read --------------------", vals1)
    #     res = super(preview_file, self).read([])
    #     return res