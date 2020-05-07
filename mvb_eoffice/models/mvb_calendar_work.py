# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class NewModule(models.Model):
    _name = 'mvb.calendar.work'
    _rec_name = 'name'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Lịch công tác'

    name = fields.Char('Chủ đề', required=True)
    employee_id = fields.Many2one(comodel_name="res.users", string="Nhân viên", required=False, default=lambda self: self.env.user, readonly=False)
    # employee_ids = fields.Many2many(comodel_name="res.users", relation="calendar_users", column1="calendar_id", column2="employee_id", string="Nhân viên", )
    content = fields.Text(string="Nội dung lịch công tác", required=False, )
    work_date_start = fields.Datetime(string="Thời gian bắt đầu", required=False, )
    work_date_end = fields.Datetime(string="Thời gian kết thúc", required=False, )
    address = fields.Char(string="Địa điểm", required=False, )

    api.constrains('employee_id')
    def get_name(self):
        for employee in self:
            employee.employee_id = self.employee_id.name

