# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MvbFile(models.Model):
    _inherit = 'muk_dms.file'
    _description = 'Quản lý nhóm tài liệu'

    list_document_of_groups = fields.Many2many(comodel_name='mvb.document', string="Danh sách tài liệu",
                                               required=False, )

    count_document = fields.Integer(string='Số lượng văn bản', compute='_count_document', readonly=True, store=True, default=0)

    @api.depends('list_document_of_groups')
    def _count_document(self):
        for rec in self:
            rec.count_document = len(rec.list_document_of_groups)

    @api.multi
    def action_groups_folder_download_attachment(self):
        tab_id = []
        if self:
            for rec in self:
                for i in rec.list_document_of_groups:
                    attachments = self.env['ir.attachment'].search(
                        [('res_model', '=', 'mvb.document'), ('res_id', '=', i.id)])
                    for attachment in attachments:
                        tab_id.append(attachment.id)
                    msg = "Tất cả file đính kèm đã được <strong>Tải xuống</strong>!"
                    i.message_post(body=msg)
            url = '/web/binary/download_document?tab_id=%s' % tab_id
            return {
                'type': 'ir.actions.act_url',
                'url': url,
                'target': 'self',
            }