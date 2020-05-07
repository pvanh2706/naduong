from odoo import api, fields, models


class settingPreview(models.Model):
    _name = 'mvb.setting.preview'
    _description = 'Model hướng dẫn sử dụng preview'

    name = fields.Char('')

    def setup_preview(self):
        if self:
            return {
                'type': 'ir.actions.act_url',
                'url': "https://chrome.google.com/webstore/detail/office-editing-for-docs-s/gbkeegbaiigmenfmjfclcdgdpimamgkj",
                'target': 'new',
            }
    @api.model
    def update_mimetype(self, id_file):
        print("self", self)
        print("type", int(id_file['id_file']))
        idFile = int(id_file['id_file'])
        res = self.env["ir.attachment"].browse(idFile)
        fileEX = ['xlsx', 'csv', 'xls']
        if res.name[res.name.rfind('.') + 1:] in fileEX:
            self._cr.execute("UPDATE ir_attachment SET mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' WHERE id = "+str(idFile))
        return 1