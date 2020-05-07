# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta, time, date
import pandas as pd
from odoo.exceptions import ValidationError


class TotalCalendar(models.TransientModel):
    _name = 'doimoi.total.calendar.wizards'
    _description = 'Tổng hợp lịch công tác của các lãnh đạo'

    name = fields.Char(string="Tuần", required=False, )

    date_from = fields.Date(string="Từ ngày", required=False,
                            default=lambda self: str(fields.datetime.today()))
    date_to = fields.Date(string="Đến ngày", required=False, readonly=True)
    state = fields.Selection(string="Trạng thái",
                             selection=[('draft', 'Nháp'), ('confirm', 'Xác nhận'), ],
                             required=False, default='confirm')
    note_2 = fields.Text(string="Ghi chú", required=False, )

    @api.onchange('date_from')
    def onchange_method(self):
        self.name = 'Tuần ' + str(int(self.date_from.strftime('%W')) + 1)
        self.date_to = self.date_from + timedelta(days=5)

    def total_calendar_leads(self):
        self.env['bus.bus'].sendmany(
            [[(self._cr.dbname, 'mail.channel', 1), {'channel_ids': 'count', 'type': 'count'}]])
        if self.date_from.strftime("%A") != 'Monday':
            raise ValidationError(_('Bạn phải chọn ngày bắt đầu là Thứ 2 đầu tuần'))
        else:
            domain = [('name', '=', self.name), ('state', '=', self.state)]
            rec = self.env['doimoi.work.calendar'].search(domain, order='sequence, employee_id')
            res = self.env['doimoi.total.calendar'].search([('name', '=', self.name)])
            to_string = ''
            if rec and (not res):
                for record in rec:
                    if to_string == '':
                        to_string = record.calendar[:record.calendar.rfind('</tbody>')]
                    else:
                        to_string += record.calendar[
                                     record.calendar.find('<tr style="background-color:'):record.calendar.rfind(
                                         '</tr>') + 5]
                values = {
                    'name': self.name,
                    'date_from': self.date_from,
                    'date_to': self.date_to,
                    'calendar': to_string + '</tbody></table>',
                    'note_2': self.note_2
                }
                rec_o = self.env['doimoi.total.calendar'].create(values)
                print('vào thông báo')
                rec_o.send_reply()
