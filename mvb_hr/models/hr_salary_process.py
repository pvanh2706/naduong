from odoo import api, fields, models


class HrSalaryProcess(models.Model):
    _name = 'hr.salary.process'
    _description = "Quá trình lương của bản thân"
    _rec_name = 'employee_id'

    time = fields.Char(string="Tháng/Năm")
    level = fields.Char(string="Ngạch/Bậc")
    coefficients_salary = fields.Float(string='Hệ số lương')

    employee_id = fields.Many2one(string="Nhân viên", comodel_name='hr.employee', required=True, ondelete='cascade')
