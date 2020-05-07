from odoo import api, fields, models, _


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.model
    def create(self, values):
        if values.get('res_model') == 'mvb.document':
            record = self.env[values.get('res_model')].search([('id', '=', values.get('res_id'))])
            msg = 'File <strong>' + values.get('datas_fname') + '</strong> được <strong>Thêm</strong> vào tài liệu'
            record.message_post(body=msg)
        return super(IrAttachment, self).create(values)

    @api.multi
    def unlink(self):
        if len(self) == 1:
            if self.res_model == 'mvb.document':
                print('test')
                if self.create_uid.id == self._uid:
                    record = self.env[self.res_model].search([('id', '=', self.res_id)])
                    msg = 'File <strong>' + self.name + '</strong> đã bị <strong>Xóa</strong> khỏi vào tài liệu'
                    record.message_post(body=msg)
                    return super(IrAttachment, self).unlink()
