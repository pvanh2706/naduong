# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.http import request
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta, time, date
import pandas as pd


class ContentCalendarEdit(models.TransientModel):
    _name = 'doimoi.content.calendar.edit.wizards'
    _description = 'Nội dung điều chỉnh lịch'

    name = fields.Char(string="", required=False, )
    note = fields.Text(string="Nội dung", required=False, )

    def send_content(self):
        self.env['bus.bus'].sendmany(
            [[(self._cr.dbname, 'mail.channel', 1), {'channel_ids': 'count', 'type': 'count'}]])
        res = self.sudo().env['doimoi.total.calendar'].browse(self._context.get('active_id'))
        res.write({'note': self.note})
        res.fix_calendar()
        # gui thong bao
        rec = self.env['res.users'].search([])
        list_user = []
        if rec:
            for record in rec:
                if record.has_group("my_calendar.group_work_calendar_leads"):
                    list_user.append(record.id)
        print(list_user)
        msg = 'Giám đốc gửi lại lịch công tác ' + res.name + '\n Nội dung: ' + str(
            res.note)
        heading_msg = "Công ty Than Núi Hồng\n"
        result = []
        search_condition = [("user_id", "in", list_user)]

        one_signal_user_object = self.env['one_signal_notification.users_device_ids'].search(
            search_condition)
        for current_record in one_signal_user_object:
            result.append(current_record.name)

        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        base_url += '/web#id=%d&view_type=form&model=%s' % (res.id, res._name)

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
