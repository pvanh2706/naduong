# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ManagementDocument(models.Model):
    _name = 'mvb.management.document'
    _description = 'Quản lý bản ghi văn bản'
    _rec_name = 'year'

    @api.multi
    def _get_count_go(self):
        self.count_go = self.env['mvb.text.go'].search_count([('text_go_book_id', '=', self.id)])

    def get_count_incoming(self):
        print('test')
        # self.count_go = self.env['mvb.text.go'].search_count([('text_go_book_id', '=', self.id)])

    def open_document_go(self):
        return {
            'name': _('Văn bản đến'),
            'domain': [('text_go_book_id', '=', self.id)],
            'view_type': 'form',
            'res_model': 'mvb.text.go',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    year = fields.Char('Sổ văn bản đến', default=lambda self: str(fields.datetime.today().year))
    count_incoming = fields.Integer(string="Số đến", required=False, compute='get_count_incoming')
    count_go = fields.Integer(string="Số văn bản đi", required=False, compute='_get_count_go')
