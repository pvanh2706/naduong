from odoo import api, fields, models


class HrFamilyRelationShip(models.Model):
    _name = 'hr.family.relationship'
    _description = 'Quan hệ gia đình'

    relationer = fields.Char(string="Quan hệ")
    full_name = fields.Char(string="Họ và tên")
    year = fields.Char(string="Năm sinh")
    infomation = fields.Text(string="Thông tin",
                             help="Quê quán, nghề nghiệp, chức danh, chức vụ, đơn vị công tác, học tập, nơi ở (trong, ngoài nước), thành viên các tổ chức chính trị - xã hội")

    employee_id1 = fields.Many2one(string="Nhân viên",comodel_name='hr.employee', ondelete='cascade')
    employee_id2 = fields.Many2one(string="Nhân viên", comodel_name='hr.employee', ondelete='cascade')