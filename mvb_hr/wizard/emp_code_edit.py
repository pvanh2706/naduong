from odoo import api, fields, models, _
from odoo.exceptions import UserError


class EmpCodeEdit(models.TransientModel):
    _name = 'hr.employee.code.edit'
    _description = 'Đổi mã nv'

    employee_code = fields.Char('Mã nhân viên')

    @api.multi
    def emp_code_edit(self):
        active_id = self.env.context.get('active_id')
        employee = self.env['hr.employee'].browse(active_id)
        employee.update({
            'employee_code':self.employee_code
        })
        return {'type': 'ir.actions.act_window_close'}
