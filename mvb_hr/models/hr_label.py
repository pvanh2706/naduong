from odoo import api, fields, models


class HrLabel(models.Model):
    _name = 'hr.label'
    _description = 'Danh hiệu được phong'

    year = fields.Char(string="Năm")
    label = fields.Char(string="Danh hiệu được phong")

    employee_id = fields.Many2one(string="Nhân viên", comodel_name='hr.employee', ondelete='cascade')
