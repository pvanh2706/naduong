from odoo import api, fields, models, _
from odoo.osv import expression
from datetime import datetime
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
from odoo import tools
from odoo import http
from odoo.http import request


class MVBTextDraftWizard(models.TransientModel):
    _name = 'mvb.text.draft.wizard'

    notes = fields.Text('Nội dung')
    name_ids = fields.Many2many(comodel_name="res.users", relation="user_receive", column1="col1", column2="col2",
                                string="Chuyến tới")
    date_direction = fields.Datetime(string="Ngày Chuyển", required=False, default=fields.Datetime.now)
    dead_line = fields.Datetime(string="Thời hạn xử lý", required=False)
    person_follow_ids = fields.Many2many(comodel_name="res.users", relation="user_draft_text_go", column1="row_1", column2="row_2",
                                         string="Người theo dõi văn bản", )
    content_direction = fields.Text('Nội dung')
    # xử lý văn bản
    def action_send_draft_text_leader(self):
        self.env['bus.bus'].sendmany(
            [[(self._cr.dbname, 'mail.channel', 1), {'channel_ids': 'count', 'type': 'count'}]])
        res = self.env['mvb.draft.text.go'].browse(self._context.get('active_id'))
        if res:
            list_user = []
            for user in self.name_ids:
                list_user.append(user.id)
                update = {
                    'state': 'pending_leader',
                    'name': user.id,
                }
                res.write(update)
                if res.check_user_create == True:
                    user_created = {
                        'user_create': self.create_uid.id,
                        'date_create': tools.datetime.now(),
                        'check_user_create': False
                    }
                    res.write(user_created)
                if user.id == self.create_uid.id:
                    raise ValidationError('Không được gửi cho chính bản thân')
                else:
                    # luu trang thai đã xử lý với 2 ng cùng được nhận 1 công việc
                    domain = [('name', '=', self.create_uid.id), ('text_ids', '=', res.id)]
                    res_status = self.env['mvb.people.processing.textdraft'].search(domain)
                    if res_status:
                        domain_send = [('name_send', '=', res_status.name_send.id), ('text_ids', '=', res.id)]
                        res_status_send = self.env['mvb.people.processing.textdraft'].search(domain_send)
                        if res_status_send:
                            for rec in res_status_send:
                                rec.state = 'daxuly'

                    domain2 = [('name', '=', user.id), ('text_ids', '=', res.id)]
                    res_check = self.env['mvb.people.processing.textdraft'].search(domain2)
                    if res_check:
                        res_check.unlink()
                        record_update1 = {
                            'name': user.id,
                            'text_ids': res.id,
                            'state': 'chuaxuly',
                            'notes': self.notes,
                            'name_send': self.create_uid.id,
                            'date_received': self.date_direction,
                            'dead_line': self.dead_line
                        }
                        res.write({'status_text': [(0, 0, record_update1)]})
                    else:
                        record_update = {
                            'name': user.id,
                            'text_ids': res.id,
                            'state': 'chuaxuly',
                            'notes': self.notes,
                            'name_send': self.create_uid.id,
                            'date_recevied': self.date_direction,
                            'dead_line': self.dead_line
                        }
                        res.write({'status_text': [(0, 0, record_update)]})

                # update theo dõi quá trình
            record_update_processing = {
                'user_send': self.create_uid.id,
                'user_received': [(6, 0, list_user)],
                'notes': self.notes,
                'textdraft_ids': res.id,
                # 'date': self.date_direction
            }
            res.write({'status_line': [(0, 0, record_update_processing)]})

            # gui thong bao
            msg = "Gửi bạn VB đi\nSố hiệu: " + \
                str(res.number_text_go) + "\nNội dung: " + \
                str(res.content_compendium)
            self.send_notify_to_user(list_user, msg, res)

    # không phê duyệt
    def action_send_draft_text_reject(self):
        print("đã vào đây,,,,,,,,,,,,,,,,,,,,,,")
        res = self.env['mvb.draft.text.go'].browse(self._context.get('active_id'))
        if res:
            list_user = []
            for user in self.name_ids:
                list_user.append(user.id)
                domain = [('name', '=', self.create_uid.id), ('text_ids', '=', res.id)]
                res_status = self.env['mvb.people.processing.textdraft'].search(domain)
                if res_status:
                    domain_send = [('name_send', '=', res_status.name_send.id), ('text_ids', '=', res.id),
                                   ('state', '=', 'chuaxuly')]
                    res_status_send = self.env['mvb.people.processing.textdraft'].search(domain_send)
                    if res_status_send:
                        for rec in res_status_send:
                            rec.state = 'daxuly'

                record_update = {
                    'name': user.id,
                    'text_ids': res.id,
                    'state': 'chuaxuly',
                    'notes': self.notes,
                    'name_send': self.create_uid.id,
                    'dead_line': self.dead_line
                }
                res.write({'status_text': [(0, 0, record_update)]})

            # update theo dõi quá trình
            record_update_processing = {
                'user_send': self.create_uid.id,
                'user_received': [(6, 0, list_user)],
                'notes': self.notes,
                'textdraft_ids': res.id,
                # 'date': self.date_direction
            }
            res.write({'status_line': [(0, 0, record_update_processing)]})
            self.env['bus.bus'].sendmany(
                [[(self._cr.dbname, 'mail.channel', 1), {'channel_ids': 'count', 'type': 'count'}]])
            
            # gui thong bao
            msg = "Không phê duyệt VB đi\nSố hiệu: " + \
                str(res.number_text_go) + "\nNội dung: " + \
                str(res.content_compendium)
            self.send_notify_to_user(list_user, msg, res)
            

    # duyệt văn bản
    def action_send_draft_text_confirm(self):
        res = self.env['mvb.draft.text.go'].browse(self._context.get('active_id'))
        if res:
            list_user = []
            for user in self.name_ids:
                list_user.append(user.id)
                update = {
                    'state': 'confirm',
                    'name': user.id,
                    'name_signed': self.create_uid.id,
                    'date_signed': tools.datetime.now()
                }
                res.write(update)

                domain = [('name', '=', self.create_uid.id), ('text_ids', '=', res.id)]
                res_status = self.env['mvb.people.processing.textdraft'].search(domain)
                if res_status:
                    res_status.state = 'dapheduyet'
                    domain_send = [('name_send', '=', res_status.name_send.id), ('text_ids', '=', res.id),
                                   ('state', '=', 'chuaxuly')]
                    res_status_send = self.env['mvb.people.processing.textdraft'].search(domain_send)
                    if res_status_send:
                        for rec in res_status_send:
                            rec.state = 'daxuly'

                record_update = {
                    'name': user.id,
                    'text_ids': res.id,
                    'state': 'chuaxuly',
                    'notes': self.notes,
                    'name_send': self.create_uid.id,
                    'dead_line': self.dead_line
                }
                res.write({'status_text': [(0, 0, record_update)]})

            # update theo dõi quá trình
            record_update_processing = {
                'user_send': self.create_uid.id,
                'user_received': [(6, 0, list_user)],
                'notes': self.notes,
                'textdraft_ids': res.id,
                # 'date': self.date_direction
            }
            res.write({'status_line': [(0, 0, record_update_processing)]})
                    # gui thong bao
            msg = "Đã phê duyệt VB đi\nSố hiệu: " + \
                str(res.number_text_go) + "\nNội dung: " + \
                str(res.content_compendium)
            self.send_notify_to_user(list_user, msg, res)


    # gui thong bao den cac user
    def send_notify_to_user(self, list_user, msg, res):
        heading_msg = "Công ty Than Na Dương\n" + \
            '[' + self.create_uid.mvb_department_name + ']' + self.create_uid.name
        result = []
        search_condition = [("user_id", "in", list_user)]
        one_signal_user_object = self.env['one_signal_notification.users_device_ids'].search(
            search_condition)

        base_url = request.env['ir.config_parameter'].sudo(
        ).get_param('web.base.url')
        base_url += '/web#id=%d&view_type=form&model=%s' % (res.id, res._name)

        for current_record in one_signal_user_object:
            result.append(current_record.name)
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

    def action_solution_direction_draft_text_go(self):
        print("self--------------------------------------", self.content_direction)
        print("self--------------------------------------", self.person_follow_ids)
        # self.env['bus.bus'].sendmany([[(self._cr.dbname, 'mail.channel', 1), {'channel_ids': 'count', 'type': 'count'}]])
        res = self.env['mvb.draft.text.go'].browse(self._context.get('active_id'))
        print("res----------", res)
        print("res----------", self._context.get('active_id'))
        print("res1-----------", self.env['mvb.draft.text.go'].search_read([('id','=',2)]))
        if res:
            list_user = []
            for user in self.person_follow_ids:
                list_user.append(user.id)
                update = {
                    'state': 'pending_leader',
                    'name': user.id,
                }
                res.write(update)
                if res.check_user_create == True:
                    user_created = {
                        'user_create': self.create_uid.id,
                        'date_create': tools.datetime.now(),
                        'check_user_create': False
                    }
                    res.write(user_created)
                if user.id == self.create_uid.id:
                    raise ValidationError('Không được gửi cho chính bản thân')
                else:
                    domain2 = [('name', '=', user.id), ('text_ids', '=', res.id)]
                    res_check = self.env['mvb.people.processing.textdraft'].search(domain2)
                    print("res_check--------------------------------", res_check)
                    if res_check:
                        res_check.unlink()
                        record_update1 = {
                            'name': user.id,
                            'text_ids': res.id,
                            'state': 'chuaxuly',
                            'notes': self.content_direction,
                            'name_send': self.create_uid.id,
                            'date_received': self.date_direction,
                            'dead_line': self.dead_line
                        }
                        res.write({'status_text': [(0, 0, record_update1)]})
                    else:
                        record_update = {
                            'name': user.id,
                            'text_ids': res.id,
                            'state': 'chuaxuly',
                            'notes': self.content_direction,
                            'name_send': self.create_uid.id,
                            'date_recevied': self.date_direction,
                            'dead_line': self.dead_line
                        }
                        res.write({'status_text': [(0, 0, record_update)]})
            record_update_processing = {
                'user_send': self.create_uid.id,
                'user_received': [(6, 0, list_user)],
                'notes': self.content_direction,
                'textdraft_ids': res.id,
                # 'date': self.date_direction
            }
            res.write({'status_line': [(0, 0, record_update_processing)]})

            # gui thong bao
            msg = "Gửi bạn VB đi\nSố hiệu: " + \
                str(res.number_text_go) + "\nNội dung: " + \
                str(res.content_compendium)
            self.send_notify_to_user(list_user, msg, res)