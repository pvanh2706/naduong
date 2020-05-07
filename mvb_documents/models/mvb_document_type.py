from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _

class DocumentType(models.Model):

    _name = 'mvb.document.type'
    _description = 'Loại tài liệu liên quan'

    name = fields.Char('Tên loại tài liệu')
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Tên loại tài liệu phải là duy nhất!')
    ]

    no_number_document = fields.Boolean("Loại tài liệu không có số hiệu văn bản", default=False)

    suffixes = fields.Char("Tên hậu tố")

    # code_number = fields.One2many(comodel_name="mvb.document.type.codenumber", inverse_name="code_number_type", string="Số hiệu văn bản", required=False, ondelete='cascade')


    @api.multi
    @api.constrains('name')
    def validate_type_document(self):
        if self.name == False:
            raise ValidationError(_('Không bỏ trống Tên tài liệu!'))


# class DocumentCodeNumberType(models.Model):
#     _name = 'mvb.document.type.codenumber'
#     _description = 'Model quản lý các mã code số hiệu tài liệu'
#
#     name = fields.Char('Tên số hiệu', readonly=True)
#     code_number_type = fields.Many2one(comodel_name="mvb.document.type", string="Loại tài liệu", required=False, readonly=True )
#
#     _sql_constraints = [
#         ('name_uniq', 'unique (name)', '(Tài liệu không có số hiệu)Số hiệu tài liệu phải là duy nhất!')
#     ]