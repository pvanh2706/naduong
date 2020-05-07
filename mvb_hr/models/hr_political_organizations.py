from odoo import api, fields, models


class HrPoliticalOrganizations(models.Model):
    _name = 'hr.political.organizations'
    _description = 'Tham gia các tổ chức chính trị, xã hội'

    date = fields.Date(string="Ngày tham gia các tổ chức chính trị, xã hội")
    name = fields.Char(string="Tên tổ chức chính trị, xã hội")

    employee_id = fields.Many2one(string="Nhân viên", ondelete='cascade')
