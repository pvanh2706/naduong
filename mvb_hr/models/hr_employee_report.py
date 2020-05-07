from odoo import api, fields, models

class HrEmployeeReport(models.Model):
    _name = 'hr.employee.report'

    name = fields.Char()
    employee_id = fields.Many2one(comodel_name="hr.employee", string="Employee", required=True, ondelete='cascade')
    label = fields.Char('Nhãn')
    job_position_group = fields.Selection(related='employee_id.job_id.job_position_group', store=True)
    job_position_level = fields.Selection(related='employee_id.job_id.job_position_level', store=True)
    job_level = fields.Selection(related='employee_id.job_id.job_level', store=True)
