# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, timedelta, time, date
from odoo.http import request


class CalendarTotal(models.Model):
    _name = 'doimoi.total.calendar'
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = 'name'
    _order = 'date_from desc'
    _description = 'Tổng hợp lịch công tác tuần'

    def _get_name_company(self):
        res = self.env['res.company'].search([('is_corporation', '=', True)])
        return res

    name = fields.Char(string='Tuần')
    calendar = fields.Html(string="Lịch công tác", )
    employee_id = fields.Many2one(comodel_name="res.users", string="Lãnh Đạo", required=False,
                                  default=lambda self: self.env.user, readonly=False)
    company_id = fields.Many2one(comodel_name="res.company", string="Công ty", required=False,
                                 default=_get_name_company)
    date_from = fields.Date(string="Từ ngày", required=False, )
    date_to = fields.Date(string="Đến ngày", required=False, )
    state = fields.Selection(string="Trạng thái",
                             selection=[('draft', 'Chưa duyệt'), ('confirm', 'Đã duyệt'), ('edit', 'Sửa lại')],
                             required=False, default='draft')
    note = fields.Text(string="Nội dung chỉnh sửa", required=False, )
    note_2 = fields.Text(string="Ghi chú", required=False, )

    def confirm(self):
        self.sudo().state = 'confirm'

    def fix_content_calendar(self):
        if self:
            form_view_id = self.env.ref('my_calendar.doimoi_total_calendar_edit_wizards_view_form').id
            return {
                'name': 'Ý kiến điều chỉnh',
                'type': 'ir.actions.act_window',
                'res_model': 'doimoi.content.calendar.edit.wizards',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': form_view_id,
                # 'context': ,
                'target': 'new',
            }

    def fix_calendar(self):
        self = self.sudo()
        self.state = 'edit'

    def send_reply(self):
        self.env['bus.bus'].sendmany(
            [[(self._cr.dbname, 'mail.channel', 1), {'channel_ids': 'count', 'type': 'count'}]])
        self.state = 'draft'
        rec = self.env['res.users'].search([])
        # gui thong bao
        list_user = []
        if rec:
            for record in rec:
                if record.has_group("my_calendar.group_work_calendar_leadership_doctor"):
                    list_user.append(record.id)
        msg = 'Trình Giám đốc xem xét duyệt lịch công tác ' + self.name

        heading_msg = "Công ty Than Núi Hồng\n"
        result = []
        search_condition = [("user_id", "in", list_user)]

        one_signal_user_object = self.env['one_signal_notification.users_device_ids'].search(
            search_condition)
        for current_record in one_signal_user_object:
            result.append(current_record.name)

        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        base_url += '/web#id=%d&view_type=form&model=%s' % (self.id, self._name)

        vals = {
            'app_id': 1,
            'specific_devices': 'include_player_ids',
            'user_ids': [(6, 0, list_user)],
            'target_parameters': result,
            'contents': {"en": msg},
            'headings': {"en": heading_msg},
            'status': 'sent',
            'included_segments': '',
            'web_url': base_url
        }
        res_notify = self.env['one.signal.notification.messages'].create(vals)
        res_notify.send_message()

    # @api.model
    # def create(self, values):
    #     print(values)
    #     # Add code here
    #     return super(CalendarTotal, self).create(values)
