# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta, time, date
import pandas as pd
from odoo.exceptions import ValidationError


class my_calendar(models.Model):
    _name = 'doimoi.work.calendar'
    _description = "Quản lý Lịch Công tác"
    _order = 'date_from desc'
    sequence = fields.Integer(string="Cấp độ hiển thị", required=False)
    name = fields.Char(string="Lịch Công tác tuần", required=False, readonly=True)
    calendar = fields.Html(string="Lịch công tác", )
    employee_id = fields.Many2one(comodel_name="res.users", string="Lãnh Đạo", required=False,
                                  default=lambda self: self.env.user, readonly=False)
    date_from = fields.Date(string="Từ ngày", required=False,
                            default=lambda self: str(fields.datetime.today()))
    date_to = fields.Date(string="Đến ngày", required=False, readonly=True)
    state = fields.Selection(string="Trạng thái",
                             selection=[('draft', 'Nháp'), ('confirm', 'Xác nhận'), ('done', 'Hoàn thành'), ],
                             required=False, default='draft')

    def confirm(self):
        self.state = 'confirm'

    @api.constrains('date_from')
    def _check_date_from(self):
        for record in self:
            if record.date_from.strftime("%A") != 'Monday':
                raise ValidationError(_('Bạn phải chọn ngày bắt đầu là Thứ 2 đầu tuần'))

    @api.onchange('date_from', 'employee_id')
    def onchange_method(self):
        color_1 = '#ffffff;'
        color_2 = '#f2f2f2;'
        _list_employye = []
        rec = self.env['res.users'].search([])
        res = self.env['res.users'].browse(self._uid)
        employee = self.env['res.users'].browse(self._uid).name
        if res.has_group("my_calendar.group_work_calendar_leadership_doctor"):
            self.sequence = 1
            _list_employye.append(color_1)
            _list_employye.append(employee)
            _list_employye.append(color_1)
        elif res.has_group("my_calendar.group_work_calendar_vice_leadership"):
            _list_user = []
            for word in rec:
                if word.has_group("my_calendar.group_work_calendar_vice_leadership"):
                    _list_user.append(word)
            if res == _list_user[2]:
                self.sequence = 2
                _list_employye.append(color_1)
                _list_employye.append(employee)
                _list_employye.append(color_1)
            else:
                self.sequence = 2
                _list_employye.append(color_2)
                _list_employye.append(employee)
                _list_employye.append(color_2)

        elif res.has_group("my_calendar.group_work_calendar_leads_office"):
            self.sequence = 3
            _list_employye.append(color_1)
            _list_employye.append(employee)
            _list_employye.append(color_1)

        my_string = '<table class="table table-bordered">\
               <tbody>\
               <tr style="text-align: center; background-color:#DBEDF4;">\
                   <th style="width: 130px;">Lãnh đạo</th>\
                    <th style="width: 60px;">Buổi</th>\
                   <th style="width: 150px;">Thứ hai</th>\
                    <th style="width: 150px;">Thứ ba</th>\
                   <th style="width: 150px;">Thứ tư</th>\
                    <th style="width: 150px;">Thứ năm</th>\
                   <th style="width: 150px;">Thứ sáu</th>\
                   <th style="width: 120px;">Thứ bảy</th>\
                   <th style="width: 120px;">Chủ nhật</th>\
                 </tr>\
                 <tr style="background-color:%s">\
                   <td rowspan="2" style="text-align: center;"><b>%s</b></td>\
                   <td>Sáng</td>\
                   <td><br></td>\
                   <td><br></td>\
                   <td><br></td>\
                   <td><br></td>\
                   <td><br></td>\
                   <td><br></td>\
                   <td><br></td>\
                 </tr>\
                 <tr style="background-color:%s">\
                   <td>Chiều</td>\
                   <td><br></td>\
                   <td><br></td>\
                   <td><br></td>\
                   <td><br></td>\
                   <td><br></td>\
                   <td><br></td>\
                   <td><br></td>\
                 </tr>\
                 </tbody>\
                 </table>' % tuple(_list_employye)

        for rec in self:
            rec.name = 'Tuần ' + str(int(rec.date_from.strftime('%W')) + 1)
            rec.date_to = rec.date_from + timedelta(days=6)
            range_date = pd.date_range(rec.date_from, rec.date_to + timedelta(days=0))
            if len(range_date) >= 7:
                my_string = my_string.replace('Thứ hai', 'Thứ hai <br> %s' % (range_date[0].strftime('%d-%m-%Y')))
                my_string = my_string.replace('Thứ ba', 'Thứ ba <br> %s' % (range_date[1].strftime('%d-%m-%Y')))
                my_string = my_string.replace('Thứ tư', 'Thứ tư <br> %s' % (range_date[2].strftime('%d-%m-%Y')))
                my_string = my_string.replace('Thứ năm', 'Thứ năm <br> %s' % (range_date[3].strftime('%d-%m-%Y')))
                my_string = my_string.replace('Thứ sáu', 'Thứ sáu <br> %s' % (range_date[4].strftime('%d-%m-%Y')))
                my_string = my_string.replace('Thứ bảy', 'Thứ bảy <br> %s' % (range_date[5].strftime('%d-%m-%Y')))
                my_string = my_string.replace('Chủ nhật', 'Chủ nhật <br> %s' % (range_date[6].strftime('%d-%m-%Y')))
                rec.calendar = my_string

    @api.model
    def create(self, values):
        rec = self.env['doimoi.work.calendar'].search_count(
            [('employee_id.id', '=', self._uid), ('date_from', '=', values.get('date_from'))])
        if rec < 1:
            return super(my_calendar, self).create(values)
        else:
            raise ValidationError(_('Không được tạo lịch công tác 2 lần trong 1 tuần! '))
