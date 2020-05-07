from odoo import api, fields, models, _
from datetime import datetime
from odoo import tools
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
import urllib3
import json
import requests
import werkzeug.urls

YEAR_NOW_DEFAULT = datetime.now().year


class MVBPeopleProcessing(models.Model):
    _name = 'mvb.people.processing.text'
    _inherit = ['mail.activity.mixin']
    _description = 'Quản lý theo dõi tình trạng của văn bản'

    text_ids = fields.Many2one(comodel_name="mvb.incoming.text", string="Văn bản", required=False, ondelete='cascade')
    person_send_id = fields.Many2one(comodel_name="res.users", string="Người gửi", required=False, )
    name = fields.Many2one(comodel_name="res.users", string="Người thực hiện", ondelete='cascade')
    state = fields.Selection(string="Tình trạng",
                             selection=[('chuaxuly', 'Chưa xử lý'), ('daxuly', 'Đã xử lý'), ('theodoi', 'Theo dõi')],
                             required=False, )
    solution_doc = fields.Char('Văn Bản')
    incoming_text_book_new = fields.Char('Sổ văn bản đến', related="text_ids.incoming_text_book")
    content_compendium = fields.Text('Trích yếu nội dung', related="text_ids.content_compendium")
    urgency = fields.Selection('Trích yếu nội dung', related="text_ids.urgency")
    received_date = fields.Date('Ngày đến', related="text_ids.received_date")
    check_unit = fields.Boolean(string="Kiểm tra theo dõi", default=True)
    check_time_view = fields.Datetime(string="Thời gian xem", required=False, )
    check_view = fields.Boolean(string="Kiểm tra truy cập", default=True)
    check_work = fields.Boolean(string="Tình trạng công việc", compute='_compute_view', store=True, default=False)
    deadline = fields.Datetime(string="Hạn xử lý", required=False, )

    @api.model
    def _needaction_domain_get(self):
        return [('state', '=', 'chuaxuly')]

    @api.multi
    @api.depends('check_view', 'state')
    def _compute_view(self):
        for rec in self:
            if rec.state == 'daxuly' and rec.check_view == False:
                rec.check_work = True

    def check_follow(self):
        self.check_view = False
        if self.check_unit == True:
            self.check_time_view = tools.datetime.now()
        self.check_unit = False

    @api.multi
    def open_mvb_incoming_text(self):
        self.check_follow()
        return {
            'name': _('Văn bản cần xử lý'),
            # 'domain': [('id','=', self.text_ids.id)],
            'res_id': self.text_ids.id,
            'view_type': 'form',
            'res_model': 'mvb.incoming.text',
            'view_id': False,
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
        }

    def document_incoming_warning_deadline_cron_job(self):
        document_now = datetime.now()
        res = self.env['mvb.people.processing.text'].search(
            [('check_work', '=', False), ('deadline', '<', document_now)])
        if res:
            for record in res:
                list_user_ids = [record.name.id]

                # gui thong bao
                msg = 'Thông báo hạn xử lý đã hết với văn bản: ' + record.text_ids.name + '</br>' + 'Trích yếu nội dung: ' + str(
                    record.content_compendium)
                print(msg)
                result = []
                search_condition = [("user_id", "in", list_user_ids)]

                one_signal_user_object = self.env['one_signal_notification.users_device_ids'].search(
                    search_condition)
                for current_record in one_signal_user_object:
                    result.append(current_record.name)

                vals = {
                    'app_id': 1,
                    'specific_devices': 'include_player_ids',
                    'user_ids': [(6, 0, list_user_ids)],
                    'target_parameters': result,
                    'contents': {"en": msg},
                    'headings': '{"en": "Công ty CN Mỏ Việt Bắc"}',
                    'status': 'sent',
                    'included_segments': ''
                }
                res_notify = self.env['one.signal.notification.messages'].create(vals)
                res_notify.send_message()


#
# Code bàng thêm
class Representative(models.Model):
    _name = 'mvb.representative'
    _rec_name = 'name_job'

    position_id = fields.Char("Chức vụ người ký")
    name_job = fields.Char("Người ký")
    company_extend_name = fields.Many2one(comodel_name="mvb.document.publisher", string="Tên Công ty", required=False,
                                          track_visibility='onchange', ondelete="cascade")


class inheritDocumentPublisher(models.Model):
    _inherit = 'mvb.document.publisher'

    representative = fields.One2many(comodel_name='mvb.representative', inverse_name='company_extend_name',
                                     string='Danh sách lãnh đạo')

    @api.model
    def create(self, values):
        # Add code here
        return super(inheritDocumentPublisher, self).create(values)


class MVBIncomingText(models.Model):
    _name = 'mvb.incoming.text'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Quản lý văn bản đến'
    _order = 'id desc'

    # lấy ra sô đến tại năm viết sổ đến

    # def get_number_incoming(self):
    #     return self.env['mvb.incoming.text'].search_count([('incoming_text_book', '=', datetime.today().year)]) + 1

    name = fields.Char('Số hiệu văn bản', track_visibility='onchange', required=True)

    incoming_text_book = fields.Char('Sổ văn bản đến', default=lambda self: str(fields.datetime.today().year),
                                     readonly=False)
    document_notebook = fields.Many2one(comodel_name="mvb.document.notebook", string="Sổ văn bản", required=False,
                                        track_visibility='onchange')

    # name_seq = fields.Char(string='Doccument_id', required=True, copy=False, readonly=True,
    #                        index=True, default=lambda self: _('New'))
    number_incoming = fields.Char('Số đến', track_visibility='onchange', readonly=False)

    received_date = fields.Date('Ngày đến', default=lambda self: str(fields.datetime.today()), readonly=False,
                                track_visibility='onchange')

    from_document_id = fields.Many2one(comodel_name="mvb.document.type", string="Hình thức văn bản",
                                       required=False,
                                       track_visibility='onchange')

    promulgate_authority = fields.Many2one(comodel_name="mvb.document.publisher", string="Cơ quan ban hành",
                                           track_visibility='onchange')
    promulgate_date = fields.Date('Ngày ban hành', default=lambda self: str(fields.datetime.today()), readonly=False,
                                  track_visibility='onchange')
    # promulgate_date = fields.Date('Ngày ban hành', track_visibility='onchange', required=True)
    content_compendium = fields.Text('Trích yếu nội dung', track_visibility='onchange')

    type_send_incoming = fields.Selection(string="Hình thức nhận",
                                          selection=[('email', 'Email'), ('fax', 'Fax'), ('post', 'Bưu Điện'),
                                                     ('portal', 'Portal'), ('eoffice', 'Eoffice')],
                                          required=False, default='eoffice')

    deadline_text = fields.Date('Hạn trả lời', track_visibility='onchange', required=False)
    attachment_ids = fields.Many2many('ir.attachment', 'car_rent_checklist_ir_attachments_rel_incoming',
                                      'rental_id', 'attachment_id', string="File đính kèm", attachment=True)
    # người ký và chức vụ onchange theo promulgate_authority
    job_signed_text = fields.Char(related='name_signed_text.position_id', string="Chức vụ")
    name_signed_text = fields.Many2one("mvb.representative", "Người ký",
                                       domain="[('company_extend_name','ilike',self.promulgate_authority.id)]")

    urgency = fields.Selection(string="Độ khẩn",
                               selection=[('thuong', 'Thường'), ('khan', 'Khẩn'), ('thuongkhan', 'Thượng khẩn'),
                                          ('hoatoc', 'Hỏa tốc'), ('hoatochengio', 'Hỏa tốc hẹn giờ')],
                               required=False, default='thuong')
    security_level = fields.Selection(string="Độ bảo mật",
                                      selection=[('mat', 'Mật'), ('domat', 'Tối mật'),
                                                 ('tuyemat', 'Tuyệt mật')], required=False, )
    number_of_received = fields.Integer('Số bản nhận')
    page_number = fields.Integer('Số trang')
    language_text = fields.Selection(string='Ngôn ngữ', selection=[('vn', 'Tiếng Việt'), ('eng', 'Tiếng Anh')],
                                     default='vn')
    note_document = fields.Text(string="Ghi chú", required=False, )
    type_document = fields.Selection(string="Loại văn bản", selection=[('draft_document', 'Bản thảo'),
                                                                       ('course_document', 'Bản chính'),
                                                                       ('course_document_same', 'Bản sao y bản chính'),
                                                                       ('document_coppy', 'Bản trích sao'),
                                                                       ('document_coppy_2', 'Bản sao lục'), ],
                                     default='course_document',
                                     required=False, )

    member = fields.One2many(comodel_name="mvb.member.direction", inverse_name="text_menber_ids",
                             string="Phân công xử lý",
                             required=False, )

    profile_ids = fields.One2many(comodel_name='mvb.job.profiles', inverse_name='incoming_text_id',
                                  string='Danh sách hồ sơ')
    # Phần quá trình xử lý
    person_receiver_ids = fields.Many2many(comodel_name="res.users", relation="rel_user4", column1="r1", column2="r2",
                                           string="Người nhận 2222", )
                                         
    person_coordinator_handles_ids = fields.Many2many(comodel_name="res.users", string="Người phối hợp xử lý",
                                                      relation="rel_user5", column1="r3", column2="r4")
    person_follow_ids = fields.Many2many(comodel_name="res.users", relation="rel_user6", column1="r5", column2="r6",
                                         string="Người theo dõi văn bản", )

    # Thông tin lưu trữ
    save_data = fields.One2many(comodel_name='mvb.document.save', inverse_name="save_text_datas_id",
                                string="Thông tin lưu trữ",
                                track_visibility='always')
    solution_data = fields.One2many(comodel_name='mvb.solution.direction', inverse_name="solution_id",
                                    string="Quá trình xử lý",
                                    track_visibility='always', readonly=True)

    is_document = fields.Boolean('Chuyển tới tài liệu dùng chung', default=False)

    state = fields.Selection(string="Trạng thái",
                             selection=[('draft', 'Đã vào sổ'), ('pending', 'Đang xử lý'), ('finish', 'Kết thúc'),
                                        ('saved', 'Lưu trữ'), ('notification', 'Thông báo')],
                             required=False, default="draft")

    status_text = fields.One2many(comodel_name="mvb.people.processing.text", inverse_name="text_ids",
                                  string="Tình trạng công việc", readonly=True, )
    # phần field action
    # active = fields.Boolean(string="Active", default=False)
    has_attachment = fields.Boolean(string='Có đính kèm?', compute='compute_has_attachment')

    active_lock = fields.Boolean(string="Check Lock", default=True)
    # display_name = fields.Char("Người nhận", compute='get_display_name')
    # # code cua Bang xư ly phan so van ban den


    # @api.multi
    # @api.depends('person_receiver_ids')
    # def get_display_name(self):
    #     for rec in self:
    #         display_name = ''
    #         count = 0
    #         print("---------------", rec.person_receiver_ids)
    #         for user in rec.person_receiver_ids:
    #             if count < 3:
    #                 display_name = display_name + user.name +','
    #                 count += 1
    #             else:
    #                 display_name = display_name + '...'
    #         rec.update({
    #             'display_name': display_name,
    #         })


    def compute_has_attachment(self):
        for em in self:
            attachments = self.env['ir.attachment'].search([('res_model', '=', 'mvb.incoming.text'), ('res_id', '=', em.id)])
            if len(attachments) > 0:
                em.has_attachment = True
            else:
                em.has_attachment = False

    @api.onchange('document_notebook')
    def change_id_text_go(self):
        domain = [('document_notebook', 'ilike', self.document_notebook.id)]
        res = self.search(domain, order="id desc")
        if res:
            for item in reversed(res):
                if item.number_incoming.isnumeric():
                    self.number_incoming = str(int(item.number_incoming) + 1)
        else:
            self.number_incoming = str(1)

    _sql_constraints = [
        # ('unique_name_incoming', 'unique(name)', 'Số hiệu văn bản đã tồn tại. \n Hãy nhập số hiệu văn bản khác'),
        ('unique_number_incoming', 'unique(number_incoming, document_notebook)',
         'Số đến văn bản đã tồn tại. \n Hãy nhập số đến văn bản khác'),
    ]

    # code mới
    @api.constrains('received_date', 'promulgate_date', 'deadline_text')
    def _check_received_date(self):
        for record in self:
            if record.received_date < record.promulgate_date:
                raise ValidationError(_('Bạn không được nhập ngày đến nhỏ hơn ngày ban hành'))

    def lock_document(self):
        self.active_lock = False

    def unlock_document(self):
        self.active_lock = True

    def solution_for_direction(self):
        self = self.sudo()
        if self:
            form_view_id = self.env.ref('mvb_eoffice.mvb_text_direction_wizard_form_solution').id
        return {
            'name': 'Chuyển xử lý VB',
            'type': 'ir.actions.act_window',
            'res_model': 'mvb.text.direction.wizard',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': form_view_id,
            'target': 'new',
        }

    def notification(self):
        self.state = "notification"
        for word in self.status_text:
            word.state = "daxuly"
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Bạn đã thông báo văn bản này cho tất cả mọi người',
                'type': 'rainbow_man',
            }
        }

    def finished(self):
        self = self.sudo()
        self.state = 'finish'

        for word in self.status_text:
            word.state = "daxuly"
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Xử lý văn bản đã kết thúc',
                'type': 'rainbow_man',
            }
        }

    def confirm_document_incoming(self):
        for item in self.status_text:
            if item.name.id == self._uid:
                item.state = 'daxuly'

    def save_mvb(self):
        print('aaa')
        url = "http://125.212.202.149:8069/web/session/authenticate/"
        # g = requests.get(url,)
        # print(g.text)
        headers_s = {'Content-type': 'application/json; charset=utf-8', 'Accept': 'text/json'}
        payload = {
            "jsonrpc": "2.0",
            "params": {
                "login": "hienlh@cmv.vn",
                "password": "1234",
                "db": "nghiem_thu"
            }
        }
        r = requests.post(url, data=json.dumps(payload), headers=headers_s)

        print(r.text)
        if r.status_code == 200:
            print('Bạn đăng nhập thành công!')
        elif r.status_code == 404:
            print('Bạn chưa thể đăng nhập thành công.')
        URL1 = 'http://125.212.202.149:8069/api/mvb.document'
        myobj = {
            "params": {
                "data": {
                    "name": "2002/CMV-VP-toan-test",
                    "document_type": "Công văn đi",
                    "name_document": "Nghỉ ngày Truyền thống ngành than 12/11",
                    "date_document": "2019-05-11",
                    "document_arrival_date": "2019-06-12",
                    "count_document": 1,
                    "unit_promulgate": "Tổng Công ty công nghiệp mỏ Việt Bắc TKV - CTCP",
                    "document_notebook": "Sổ văn bản đi 2019",
                    "share_user": "admin@gmail.com,hienlh@cmv.vn",
                    "eGov": "True",
                    "create_by": "admin@gmail.com",
                    "data_attachment": [
                        {
                            "name_attachment": "Test.pdf",
                            "data_file_base64": "content"
                        },
                        {
                            "name_attachment": "Test1.pdf",
                            "data_file_base64": "content"
                        },
                        {
                            "name_attachment": "Test2.pdf",
                            "data_file_base64": "content"
                        }
                    ]
                }
            }
        }
        print(r.cookies)
        response = requests.post(URL1, data=json.dumps(myobj), headers=headers_s, cookies=r.cookies)
        print(response.text)
        if response.status_code == 200:
            print('Success!')
        elif response.status_code == 404:
            print('Not Found.')

    # @api.model
    # def create(self, values):
    #     r = str(self.env['mvb.incoming.text'].search_count(
    #         [('incoming_text_book', '=', datetime.today().year)])+1)
    #     rec_update = {'number_incoming': r}
    #
    #     values.update(rec_update)
    #
    #     res = super(MVBIncomingText, self).create(values)
    #
    #     return res

    def push_data_for_document(self):

        self.state = "saved"
        _list_ids = []
        for word in self.status_text:
            _list_ids.append(word.name.id)
        vals = {
            'name': self.name,
            'document_type': self.from_document_id.id,
            'name_document': self.content_compendium,
            'date_document': str(self.promulgate_date),
            'document_arrival_date': self.received_date,
            'count_document': self.page_number,
            'unit_promulgate': self.promulgate_authority.id,
            'document_notebook': self.document_notebook.id,
            'share_user': [(6, 0, _list_ids)],
        }
        res = self.env['mvb.document'].create(vals)
        rec = self.env['ir.attachment'].search([('res_id', '=', self.id)])
        if rec:
            for item in rec:
                self.env['ir.attachment'].create([{'name': item.name,
                                                   'datas': item.datas,
                                                   'datas_fname': item.name, 'res_model': 'mvb.document',
                                                   'res_id': res.id}])
        if self.attachment_ids:
            for word in self.attachment_ids:
                self.env['ir.attachment'].create([{'name': word.name,
                                                   'datas': word.datas,
                                                   'datas_fname': word.name, 'res_model': 'mvb.document',
                                                   'res_id': res.id}])

    @api.model
    def create(self, values):
        print(values)
        # Add code here
        res = super(MVBIncomingText, self).create(values)
        return res

    # @api.onchange('promulgate_authority')
    # def _onchange_promulgate_authority(self):
    #     domain = [("company_extend_name","ilike",self.promulgate_authority.id)]
    #     res = self.env['mvb.representative'].search(domain, limit=1)
    #     print("ressssssssssssssssssss",res)
    #     for item in res:

    # @api.model
    # def create(self, vals):
    #     if vals.get('name_seq', _('New')) == _('New'):
    #         vals['name_seq'] = self.env['ir.sequence'].next_by_code('mvb.incoming.text.sequence') or _(0)
    #     result = super(MVBIncomingText, self).create(vals)
    #     return result
    # Tự động ẩn hiện bản ghi theo định kỳ
    # def hide_cron_job(self):
    #     """
    #     hàm ẩn bản ghi của văn bản đi
    #     """
    #     s = self.env['mvb.incoming.text'].search([('incoming_text_book_id', '<', datetime.today().year)])
    #     for word in s:
    #         if word.active is True:
    #             word.write({'active': False})

    # def appear_cron_job(self):
    #     s = self.env['mvb.incoming.text'].search([('active', '=', False)])
    #     print(s)
    #     for i in s:
    #         i.write({'active': True})
    # @api.multi
    # def write(self, values):
    #     # res = self.env["res.users"].search([])
    #     # list_partner_id = []
    #     # for user in res:
    #     #     if user.has_group(
    #     #             "mvb_eoffice.group_incoming_text_office_leadership"
    #     #     ):
    #     #         list_partner_id.append(user)
    #     #
    #     # if self.env["res.users"].browse(self._uid) in list_partner_id:
    #     #     raise ValidationError('Ban khong co quyen duoc sua')
    #
    #     return super(MVBIncomingText, self).write(values)
    @api.onchange('received_date')
    def get_document_notebook_come(self):
        domain = [("year_doc", "=", YEAR_NOW_DEFAULT), ("type_doc", "=", "đến")]
        res = self.env['mvb.document.notebook'].search(domain)
        domain1 = [('document_notebook', 'ilike', res.id)]
        res_number_incoming = self.search(domain1, order="id desc")
        if res_number_incoming:
            for item in reversed(res_number_incoming):
                if item.number_incoming.isnumeric():
                    self.number_incoming = str(int(item.number_incoming) + 1)
        else:
            self.number_incoming = str(1)
        self.document_notebook = res.id
