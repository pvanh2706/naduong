from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT,\
    DEFAULT_SERVER_DATETIME_FORMAT

class DocumentRent(models.Model):
    _name = 'mvb.document.rent'
    _description = 'Danh mục lấy tài liệu'

    name = fields.Date('Ngày lấy')
    human_rent = fields.Many2one(comodel_name="res.users", string="Nhân sự lấy")
    number_rent = fields.Integer('Số bản lấy')
    return_date = fields.Date('Ngày bàn giao')
    rent_ids = fields.Many2one('mvb.document', 'Tài liệu mượn')

    @api.multi
    @api.constrains('name','human_rent','return_date')
    def validate_rent(self):
        if self.name == False:
            raise ValidationError(_("Không được để trống ngày lấy tài liệu!"))
        if len(self.human_rent) == 0:
            raise ValidationError(_('Không được để trống người lấy tài liệu!'))
        if self.return_date:
            start_date = datetime.strptime(str(self.name),DEFAULT_SERVER_DATE_FORMAT)
            end_date = datetime.strptime(str(self.return_date),DEFAULT_SERVER_DATE_FORMAT)
            daysDiff = (end_date - start_date).days
            if daysDiff < 0:
                raise ValidationError(_('Ngày trả phải lớn hơn ngày lấy!'))

    @api.model
    def create(self, values):
        # Add code here
        msg = ''
        res =  super(DocumentRent, self).create(values)
        if res.human_rent.name:
            msg = msg + ('<li> Nhân sự lấy: %s </li>') % (res.human_rent.name)
        if res.name:
            msg = msg + ('<li> Ngày lấy: %s </li>') % (res.name)
        if res.return_date:
            msg = msg + ('<li> Ngày trả: %s </li>') % (res.return_date)
        if res.number_rent:
            msg = msg + ('<li> Số bản lấy: %s </li>') % (res.number_rent)
        if msg != '':
            new_meg = ('<p>Tạo mới</p>')
            new_meg = new_meg + msg
            res.rent_ids.message_post(body=new_meg)
        return res

    @api.multi
    def write(self, values):
        # Add code here
        res = super(DocumentRent, self).write(values)
        update_msg = []
        if values.get('name') != None:
            msg_date_rent = ('<li>Ngày mượn: %s</li>') % str(values.get('name'))
            update_msg.append(msg_date_rent)

        if values.get('return_date') != None:
            msg_date_return = ('<li>Ngày trả: %s</li>') % str(values.get('return_date'))
            update_msg.append(msg_date_return)

        if values.get('number_rent') != None:
            msg_number_rent = ('<li>Số bản lấy: %s</li>') % str(values.get('number_rent'))
            update_msg.append(msg_number_rent)

        if values.get('human_rent') != None:
            if values.get('human_rent') == self.human_rent.id:
                msg_human_rent = ('<li>Người lấy tài liệu: %s</li>') % self.human_rent.name
                update_msg.append(msg_human_rent)

        if len(update_msg) > 0:
            msg = ('<p>Cập nhật lấy tài liệu:<p><ul>')
            for i in update_msg:
                msg = msg + i
            msg = msg + '</ul>'
            self.rent_ids.message_post(body=msg)
        return res

    @api.model
    def unlink(self):
        name_human_rent = self.human_rent
        if name_human_rent != None:
            name_rent = self.env['res.users'].browse(name_human_rent.id).name
            if name_rent != None:
                msg = ('<p>Xóa bản ghi lấy tài liệu:</p>'
                       '<ul>'
                       '<li> Nhân sự lấy tài liệu: %s </li>'
                       '<li> Ngày lấy: %s</li>'
                       '<li> Ngày trả: %s</li>'
                       '<li> Số bản lấy: %s</li>'
                       '</ul>') % (name_rent, self.name, self.return_date, self.number_rent)
                self.rent_ids.message_post(body=msg)
        res = super(DocumentRent, self).unlink()
        return res

