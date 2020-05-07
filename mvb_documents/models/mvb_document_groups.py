from odoo import api, fields, models
import time
from odoo.exceptions import UserError, ValidationError
from odoo.osv import osv
from odoo.tools.translate import _


class MVBDocumentDirectory(models.Model):
    _name = 'mvb.document.groups'
    _description = 'Quản lý danh sách các thư mục con hiển thị'

    name = fields.Char(string="Tên nhóm", required=True, index=True)

    list_document_of_groups = fields.Many2many(comodel_name="mvb.document",  string="Danh sách tài liệu", )

    @api.multi
    def action_groups_download_attachment(self):
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


