from odoo import api, fields, models


class HrNgachCongChuc(models.Model):
    _name = 'hr.ngach.cong.chuc'
    _description = 'Ngạch công chức'

    name = fields.Char(string="Tên Ngạch")
    code = fields.Char(string="Mã số")
