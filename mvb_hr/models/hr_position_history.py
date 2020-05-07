from odoo import fields, models, api
from datetime import datetime


class HrPositionHistory(models.Model):
    _name = 'hr.position.history'
    _description = 'Quá trình công tác'

    name = fields.Char(related='employee_id.name', string="Tên")
    position_id = fields.Char(string='Chức danh, chức vụ, đơn vị công tác', required=True)
    date = fields.Char('Từ tháng/năm', required=True)
    employee_id = fields.Many2one('hr.employee', 'Nhân viên', required=True, ondelete='cascade')
    description = fields.Char('Mô tả')
    date_to = fields.Char("Đến tháng/năm")
