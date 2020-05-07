from odoo import api, fields, models, _
from odoo.osv import expression
from ast import literal_eval
from odoo.exceptions import ValidationError
from odoo import http
from odoo.http import request


class MVBTextDirectionWizard(models.TransientModel):
    _name = 'mvb.text.direction.wizard'

    person_ship = fields.Many2one(comodel_name="res.users", string="Người chuyển", required=True,
                                  default=lambda self: self.env.user.id or False, ondelete='cascade')
    doctor_position = fields.Selection(string="Lãnh đạo",
                                       selection=[('doctor', 'Giám đốc')],
                                       required=False, default='doctor')
    lead_position = fields.Selection(string="Chánh văn phòng",
                                     selection=[('lead', 'Chánh văn phòng')],
                                     required=False, default='lead')
    person_feedback = fields.Selection(string="Phản hồi", selection=[('feedback', 'Trả lời'), ], default='feedback')
    document_position = fields.Selection(string="Văn thư",
                                         selection=[('document', 'Văn thư')],
                                         required=False, default='document')
    # sent_user = fields.Many2one(comodel_name="res.users", string="Lãnh đạo", required=False, )
    content_direction = fields.Text('Nội dung')

    date_direction = fields.Datetime(
        string="Ngày chuyển", required=False, default=fields.Datetime.now)
    deadline = fields.Datetime(
        string="Hạn xử lý", required=False, )
    person_receiver_ids = fields.Many2many(comodel_name="res.users", relation="rel_userd4", column1="r1", column2="r2",
                                           string="Người xử lý chính", )
    person_coordinator_handles_ids = fields.Many2many(comodel_name="res.users", string="Người phối hợp xử lý",
                                                      relation="rel_usere5", column1="r3", column2="r4")
    person_follow_ids = fields.Many2many(comodel_name="res.users", relation="rel_userf6", column1="r5", column2="r6",
                                         string="Người theo dõi văn bản", )
    add_multi_user = fields.Selection(
        [('receiver', 'Người xử lý chính'), ('coordinator', 'Người phối hợp xử lý'),
         ('follow', 'Người theo dõi văn bản'), ],
        string="Chọn người gửi", default='receiver')
    check = fields.Boolean('Kiểm tra', default=True)

    @api.constrains('person_receiver_ids', 'person_coordinator_handles_ids', 'person_follow_ids')
    def check_user(self):
        if len(self.person_receiver_ids) == 0 and len(self.person_coordinator_handles_ids) == 0 and len(self.person_follow_ids) == 0:
            raise ValidationError('Bạn phải chọn người cần gửi!')

        _list = []
        for r in self.person_receiver_ids:
            _list.append(r)
        for c in self.person_coordinator_handles_ids:
            if c in _list:
                raise ValidationError('Chọn trùng với người xử lý chính')
            else:
                _list.append(c)
        for f in self.person_follow_ids:
            if f in _list:
                raise ValidationError(
                    'Chọn trùng với người xử lý chính hoặc người phối hợp xử lý')

    @api.onchange('person_receiver_ids', 'document_position', 'doctor_position', 'person_feedback')
    def check_send_position(self):
        # check_person_reply
        if self.person_feedback == 'feedback':
            res = self.sudo().env['mvb.incoming.text'].browse(self._context.get('active_id'))
            for i in res.status_text:
                if i.name.id == self._uid:
                    self.person_receiver_ids = i.person_send_id
        # check_person_receiver_ids
        for word in self:
            if len(self.person_receiver_ids) > 1:
                word.check = False
        if self.doctor_position == 'doctor':
            res = self.env['res.users'].search(
                [('mvb_job_name', '=', 'Giám đốc')])
            rec = self.env['res.users'].search(
                [('mvb_job_name', '=', 'Chánh văn phòng')])
            if res:
                self.person_receiver_ids = res
                # self.person_follow_ids = rec

        # check_send_position
       #res_doctor = self.env['res.users'].search(
        #     [('id', '=', self._uid), ('mvb_job_name', '=', 'Giám đốc')])
        # res = self.env['res.users'].search([('mvb_job_name', '=', 'Giám đốc')])
        # if self.document_position == 'document' and res_doctor:
        #     res_document = self.env['res.users'].search(
        #         [('mvb_job_name', '=', 'Văn thư')])
        #     print(res_document)
        #     rec = self.env['res.users'].search(
        #         [('mvb_job_name', '=', 'Chánh văn phòng')])
        #     if res and res_document:
        #         self.person_receiver_ids = res_document
        #         self.person_follow_ids = rec

    def action_solution_direction(self):
        """
        function solution document
        :return:
        """
        self.env['bus.bus'].sendmany(
            [[(self._cr.dbname, 'mail.channel', 1), {'channel_ids': 'count', 'type': 'count'}]])
        res = self.sudo().env['mvb.incoming.text'].browse(self._context.get('active_id'))
        res.state = "pending"
        res_solu = self.env['mvb.solution.direction'].search([('solution_id', '=', res.id), ('person_receiver_ids', '=', self._uid), ], limit=1)
        res_peo = self.env['mvb.people.processing.text'].search([('text_ids', '=', res.id)])
        res_solution = self.env['mvb.solution.direction'].search([('solution_id', '=', res.id)])
        for k in res_solution:
            if len(k.person_receiver_ids) == 1 and (
                    self.env['res.users'].browse(self._uid) in k.person_receiver_ids):
                # Khi chuyển xủ lý thì người đang xủ lý sẽ trở thành người đã xử lý
                for i in res_solu.person_receiver_ids:
                    for word in res_peo:
                        if i == word.name:
                            word.state = "daxuly"
                for i in res_solu.person_coordinator_handles_ids:
                    for word in res_peo:
                        if i == word.name:
                            word.state = "daxuly"
            else:
                for word in res_peo:
                    if word.name.id == self._uid:
                        word.state = "daxuly"

        _list = []
        for k in res.status_text:
            _list.append(k.name)
        if res:
            # Người tạo văn bản đến
            if self.create_uid not in _list:
                if res.create_uid == self.create_uid:
                    print('Tại sao lại không vào')
                    record_update = {
                        'name': res.create_uid.id,
                        'text_ids': res.id,
                        'state': 'daxuly',
                        'check_view': False,
                        'check_work': True
                    }
                    res.write({'status_text': [[0, 0, record_update]]})
        if len(self.person_receiver_ids) <= 1:
            # Người xử lý chính
            # chuyen vao mvb.people.processing.text
            if len(self.person_receiver_ids) > 0:
                list_user_1 = []
                for i in self.person_receiver_ids:
                    list_user_1.append(i.id)

                    if i.id == self.create_uid.id or i.id == self._uid:
                        raise ValidationError(
                            'Không được gửi cho chính bản thân')
                    if i in _list:
                        for word in res.status_text:
                            if word.name in self.person_receiver_ids:
                                word.state = "chuaxuly"
                                word.write({'person_send_id': self._uid})
                                word.deadline = self.deadline
                    else:
                        record_update_new = {
                            'person_send_id': self._uid,
                            'name': i.id,
                            'text_ids': res.id,
                            'deadline': self.deadline,
                            'state': 'chuaxuly'
                        }
                        res.write({'status_text': [[0, 0, record_update_new]]})

                # gui thong bao
                msg = 'Gửi yêu cầu xử lý VBĐ\nSố hiệu: ' + res.name + '\nTYND: ' + str(
                    res.content_compendium)
                self.send_notify_users(list_user_1, msg, res)

            # chuyen du lieu vao mvb.solution.direction
            rec = []
            if len(self.person_receiver_ids) > 0:
                for i in self.person_receiver_ids:
                    rec.append(i.id)
            # Người cùng xử lý
            # chuyen vao mvb.people.processing.text
            if len(self.person_coordinator_handles_ids) > 0:
                list_user_3 = []
                for i in self.person_coordinator_handles_ids:
                    list_user_3.append(i.id)
                    if i.id == self.create_uid.id or i.id == self._uid:
                        raise ValidationError(
                            'Không được gửi cho chính bản thân')
                    if i in _list:
                        for word in res.status_text:
                            if word.name in self.person_coordinator_handles_ids:
                                word.state = "chuaxuly"
                                word.write({'person_send_id': self._uid})
                                word.deadline = self.deadline
                    else:
                        record_update_new = {
                            'person_send_id': self._uid,
                            'name': i.id,
                            'text_ids': res.id,
                            'deadline': self.deadline,
                            'state': 'chuaxuly'
                        }
                        res.write({'status_text': [[0, 0, record_update_new]]})
                msg = 'Mời bạn cùng xử lý\nSố hiệu: ' + res.name + '\nTYND: ' + str(
                    res.content_compendium)
                self.send_notify_users(list_user_3, msg, res)
            # chuyen du lieu vao mvb.solution.direction
            rec_coordinator = []
            if len(self.person_coordinator_handles_ids) > 0:
                for i in self.person_coordinator_handles_ids:
                    rec_coordinator.append(i.id)
            # Người theo dõi
            # chuyen vao mvb.people.processing.text
            if len(self.person_follow_ids) > 0:
                list_user_4 = []
                for i in self.person_follow_ids:
                    list_user_4.append(i.id)
                    if i.id == self.create_uid.id or i.id == self._uid:
                        raise ValidationError(
                            'Không được gửi cho chính bản thân')
                    if i in _list:
                        for word in res.status_text:
                            if word.name in self.person_coordinator_handles_ids:
                                word.state = "theodoi"
                                word.write({'person_send_id': self._uid})
                    else:
                        record_update_new = {
                            'name': i.id,
                            'text_ids': res.id,
                            'state': 'theodoi'
                        }
                        res.write({'status_text': [[0, 0, record_update_new]]})
                msg = 'Mời bạn theo dõi VB đến\nSố hiệu:' + res.name + '\nTYND' + str(
                    res.content_compendium)
                self.send_notify_users(list_user_4, msg, res)

            text_follow_ids = []
            if len(self.person_follow_ids) > 0:
                for i in self.person_follow_ids:
                    text_follow_ids.append(i.id)

            update_data = {
                'solution_data': [(0, 0, {
                    'content_solution': self.content_direction,
                    'person_ship': self.person_ship.id,
                    'date_start_ship': self.date_direction,
                    'date_deadline': self.deadline,
                    'person_receiver_ids': [(6, 0, rec)],
                    'person_coordinator_handles_ids': [(6, 0, rec_coordinator)],
                    'person_follow_ids': [(6, 0, text_follow_ids)],
                    'solution_id': res.id,
                })]
            }
            res.write(update_data)
            return res
        else:
            # Người xử lý chính
            # chuyen vao mvb.people.processing.text
            if len(self.person_receiver_ids) > 0:
                list_user_2 = []
                for i in self.person_receiver_ids:
                    list_user_2.append(i.id)
                    if i.id == self.create_uid.id or i.id == self._uid:
                        raise ValidationError(
                            'Không được gửi cho chính bản thân')
                    if i in _list:
                        for word in res.status_text:
                            if word.name in self.person_receiver_ids:
                                word.state = "chuaxuly"
                                word.write({'person_send_id': self._uid})
                                word.deadline = self.deadline
                    else:
                        record_update_new = {
                            'person_send_id': self._uid,
                            'name': i.id,
                            'text_ids': res.id,
                            'state': 'chuaxuly'
                        }
                        res.write({'status_text': [[0, 0, record_update_new]]})
                msg = 'Mời bạn xử lý VB đến\nSố hiệu: ' + res.name + '\nTYND: ' + str(
                    res.content_compendium)
                self.send_notify_users(list_user_2, msg, res)
                # chuyen du lieu vao mvb.solution.direction
                rec = []
                if len(self.person_receiver_ids) > 0:
                    for i in self.person_receiver_ids:
                        rec.append(i.id)
            # Người theo dõi
            # chuyen vao mvb.people.processing.text
            if len(self.person_follow_ids) > 0:
                list_user_5 = []
                for i in self.person_follow_ids:
                    list_user_5.append(i.id)
                    if i.id == self.create_uid.id or i.id == self._uid:
                        raise ValidationError(
                            'Không được gửi cho chính bản thân')
                    if i in _list:
                        for word in res.status_text:
                            if word.name in self.person_coordinator_handles_ids:
                                word.state = "theodoi"
                                word.write({'person_send_id': self._uid})
                    else:
                        record_update_new = {
                            'name': i.id,
                            'text_ids': res.id,
                            'state': 'theodoi'
                        }
                        res.write({'status_text': [[0, 0, record_update_new]]})
                msg = 'Mời bạn theo dõi VB đến\nSố hiệu: ' + res.name + '\nTYND: ' + str(
                    res.content_compendium)
                self.send_notify_users(list_user_5, msg, res)
            text_follow_ids = []
            if len(self.person_follow_ids) > 0:
                for i in self.person_follow_ids:
                    text_follow_ids.append(i.id)

            update_data = {
                'solution_data': [(0, 0, {
                    'content_solution': self.content_direction,
                    'person_ship': self.person_ship.id,
                    'date_start_ship': self.date_direction,
                    'date_deadline': self.deadline,
                    'person_receiver_ids': [(6, 0, rec)],
                    'person_follow_ids': [(6, 0, text_follow_ids)],
                    'solution_id': res.id,
                })]
            }
            res.write(update_data)

        return res

    def send_notify_users(self, list_user, msg, res):
        heading_msg = "Công ty Than Na Dương\n" + '[' + self.person_ship.mvb_department_name + ']' + self.person_ship.name
        result = []
        search_condition = [("user_id", "in", list_user)]
        one_signal_user_object = self.env['one_signal_notification.users_device_ids'].search(
            search_condition)
        for current_record in one_signal_user_object:
            result.append(current_record.name)

        base_url = request.env['ir.config_parameter'].sudo(
        ).get_param('web.base.url')
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
