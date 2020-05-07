
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _

class DocumentCodeStorage(models.Model):
    _name = 'mvb.document.code.storage'
    _description = 'Danh mục mã lưu trữ'

    name = fields.Char('Mã lưu kho', track_visibility='onchange')

    @api.multi
    @api.constrains('name')
    def _validate_name_storage(self):
        if self.name == False:
            raise ValidationError(_("Tên mã lưu kho không được bỏ trống!"))


class DocumentStorage(models.Model):
    _name = 'mvb.document.storage'
    _description = 'Danh mục lưu trữ'

    name = fields.Many2one(comodel_name='mvb.document.code.storage', string='Mã lưu kho')
    number_storage = fields.Integer('Số bản lưu')
    human_resources_saved = fields.Many2one(comodel_name='res.users', string="Nhân sự lưu kho")
    date_storage = fields.Date('Ngày lưu kho')
    storage_datas = fields.Many2one(comodel_name="mvb.document", string="Tài liệu", required=False, )
    type_document_storage = fields.Selection(string="Loại tài liệu lưu", selection=[('bangoc', 'Bản gốc'),
                                                                                    ('banchinh','Bản chính'),
                                                                                    ('bansaoybanchinh', 'Bản sao y bản chính'),
                                                                                    ('banchichsao', 'Bản trích sao'),
                                                                                    ('bansaoluc', 'Bản sao lục'), ])

    @api.one
    @api.constrains('name','human_resources_saved','date_storage')
    def _validate_data_storage(self):
        if len(self.name) == 0:
            raise ValidationError(_("Tên mã lưu kho không được bỏ trống!"))
        if self.number_storage <= 0:
            raise ValidationError(_("Số bản lưu phải lớn hơn 0!"))
        if len(self.human_resources_saved) == 0:
            raise ValidationError(_("Không được bỏ trống nhân sự lưu kho!"))
        if self.date_storage == False:
            raise ValidationError(_("Không được bỏ trống ngày lưu kho!"))

    @api.model
    def create(self, values):
        # Add code here
        msg = ''
        res = super(DocumentStorage, self).create(values)
        if res.name.name:
            msg = msg + ('<li> Mã lưu kho: %s </li>') % (res.name.name)
        if res.number_storage:
            msg = msg + ('<li> Số bản lưu: %s </li>') % (res.number_storage)
        if res.human_resources_saved:
            msg = msg + ('<li> Nhân sư lưu: %s </li>') % (res.human_resources_saved.name)
        if res.date_storage:
            msg = msg + ('<li> Ngày lưu kho: %s </li>') % (res.date_storage)
        if msg != '':
            msg_new = ('<p>Tạo mới bản ghi lưu trữ:</p>')
            msg_new = msg_new + msg
            res.storage_datas.message_post(body=msg_new)
        return res

    @api.multi
    def write(self, values):
        # Add code here
        res = super(DocumentStorage, self).write(values)

        update_msg = []
        if values.get('name') != None:
            id = int(values.get('name'))
            new_name = self.env['mvb.document.code.storage'].browse(id).name
            if new_name != None:
                msg_name = ('<li>Mã lưu kho: %s') % new_name
                update_msg.append(msg_name)

        if values.get('number_storage') != None:
            msg_number_storage = ('<li>Số bản lưu: %s</li>') % str(values.get('number_storage'))
            update_msg.append(msg_number_storage)
        #
        if values.get('human_resources_saved') != None:
            id = values.get('human_resources_saved')
            res_user_name = self.env['res.users'].browse(int(id)).name
            if res_user_name != '':
                msg_user_storage = ('<li>Nhân sự lưu: %s</li>') % res_user_name
            update_msg.append(msg_user_storage)

        if values.get('date_storage') != None:
            msg_date_storage  = ('<li>Ngày lưu kho: %s</li>') % values.get('date_storage')
            update_msg.append(msg_date_storage)

        if len(update_msg) > 0:
            msg = ('<p>Cập nhật lưu trữ tài liệu:<p>')
            for i in update_msg:
                msg = msg + i
            self.storage_datas.message_post(body=msg)
        return res

    @api.model
    def unlink(self):
        msg = ''
        if self.name.name != None:
            msg = msg + ('<li>Mã lưu kho: %s</li>') % self.name.name
        if self.number_storage != None:
            msg = msg + ('<li>Số bản lưu: %s</li>') % str(self.number_storage)
        if self.human_resources_saved.name !=None:
            msg = msg + ('<li>Nhân sự lưu kho: %s</li>') % self.human_resources_saved.name
        if self.date_storage != None:
            msg = msg + ('<li>Ngày lưu kho: %s</li>') % self.date_storage
        if msg != None:
            message = '<p>Xóa thông tin lưu trữ:</p>'
            message = message + msg
            self.storage_datas.message_post(body=message)
        res = super(DocumentStorage, self).unlink()
        return res
