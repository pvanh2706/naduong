from odoo import api, fields, models
from odoo.osv import expression
from datetime import datetime
import datetime
YEAR_NOW_DEFAULT = datetime.datetime.now().year


class inheritDocument(models.Model):
    _inherit = "mvb.document"

    mvb_text_go_ids = fields.Many2one(comodel_name="mvb.text.go", string="ID text go", store=True, invisiable=True)
    # @api.onchange('mvb_text_go_ids')
    # def _onchange_for_text_go(self):
    #     self.name_document  = self.mvb_text_go_ids.content_compendium
    #     self.document_type = self.mvb_text_go_ids.text_go_type
    #     self.name = self.mvb_text_go_ids.name
    #     self.date_document = self.mvb_text_go_ids.date_signed_text
    #     self.document_arrival_date = self.mvb_text_go_ids.delivery_date
    #     self.count_document = self.mvb_text_go_ids.page_number
    #     list_user = []
    #     list_user.append(self.env.uid)
    #     for user in self.mvb_text_go_ids.member:
    #         if user:
    #             list_user.append(user.name_employee.id)
    #     self.share_user = [(6, 0, list_user)]


class MVBTextgoForEmployee(models.Model):
    _name = "mvb.text.go.for.employee"
    _description = 'Gửi văn bản trong nội bộ công ty'

    name_employee = fields.Many2one(comodel_name="res.users", string="Tên nhân viên", ondelete="cascade")
    department = fields.Char(string="Phòng ban", related="name_employee.mvb_department_name")
    possition = fields.Char(string="Chức vụ", related="name_employee.mvb_job_name")
    email = fields.Char(string="Email", related="name_employee.login")
    number_of_received = fields.Integer('Số bản nhận')
    text_go_type_send = fields.Selection([
        ('email', 'Email'),
        ('fax', 'Fax'),
        ('post', 'Bưu điện'),
        ('portal', 'Portal'),
        ('eoffice', 'E-Office'),
        ('mvb', 'Nội bộ'),
    ], string='Hình thức gửi', default='mvb')
    text_go_ids_employee = fields.Many2one(comodel_name="mvb.text.go", string="Văn bản", ondelete="cascade",
                                           invisiable="1")


class MVBTextgoForCompanyExternal(models.Model):
    _name = "mvb.text.go.for.company.external"
    _description = 'Gửi văn bản tới công ty ngoài'
    _rec_name = "company_name"

    company_name = fields.Many2one(comodel_name="mvb.document.publisher", string="Tên công ty", required=False, )
    # company_add = fields.Char(string='Địa chỉ')
    number_of_received = fields.Integer('Số bản nhận')
    text_go_type_send = fields.Selection([
        ('email', 'Email'),
        ('fax', 'Fax'),
        ('post', 'Bưu điện'),
        ('portal', 'Portal'),
        ('eoffice', 'E-Office'),
    ], string='Hình thức gửi', default='email')
    text_go_ids_company = fields.Many2one(comodel_name="mvb.text.go", string="Văn bản", ondelete="cascade",
                                          invisiable="1")


class MVBTextGo(models.Model):
    _name = 'mvb.text.go'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Quản lý văn bản đi'
    _order = "id_text_go desc"
    _rec_name = "id_text_go"

    # text_go_book = fields.Char(string="Sổ văn bản đi", required=False,
    #                            default=lambda self: str(fields.datetime.today().year))
    # def get_notebook(self):
    #     self.
    text_go_notebook = fields.Many2one(comodel_name="mvb.document.notebook", string="Sổ văn bản", required=False,
                                       track_visibility='onchange',)
    name = fields.Char('Số hiệu văn bản', track_visibility='onchange', required=True)
    id_text_go = fields.Char('Số đi', track_visibility='onchange', readonly=True)
    delivery_date = fields.Date('Ngày đi', track_visibility='onchange', default=fields.date.today())
    text_go_type = fields.Many2one(comodel_name='mvb.document.type', string='Hình thức văn bản')
    text_go_notes = fields.Text('Ghi chú', track_visibility='onchange')

    promulgate_authority = fields.Many2one(string='Cơ quan ban hành', comodel_name='mvb.document.publisher')
    promulgate_date = fields.Date('Ngày ban hành', track_visibility='onchange', required=True, default=fields.date.today())
    content_compendium = fields.Text('Trích yếu nội dung', track_visibility='onchange', )
    deadline_text = fields.Date('Thời hạn giải quyết', track_visibility='onchange', required=False)
    draft_text_id = fields.Many2one(comodel_name="mvb.draft.text.go", string="Tạo từ văn bản dự thảo")
    date_signed_text = fields.Date('Ngày ký văn bản', track_visibility='onchange', required=True, )
    name_signed_text = fields.Many2one(comodel_name="res.users", string="Họ tên người ký văn bản", required=False, )
    job_signed_text = fields.Char(string="Chức vụ người ký văn bản", related="name_signed_text.mvb_job_name")

    user_create = fields.Many2one(comodel_name="res.users", string="Người tạo văn bản", )
    date_create = fields.Date(string="Ngày tạo", )
    department_create = fields.Char('Phòng ban', )
    job_create = fields.Char('Chức vụ', )

    state = fields.Selection([('waitting', 'Đang chờ lưu trữ'),
                              ('saved', 'Đã lưu trữ')], required=True, default="waitting")

    urgency = fields.Selection([
        ('thuong', 'Thường'),
        ('khan', 'Khẩn'),
        ('thuongkhan', 'Thượng khẩn'),
        ('hoatoc', 'Hỏa tốc'),
        ('hoatochengio', 'Hỏa tốc hẹn giờ'),
    ], string='Độ khẩn', default="thuong")

    security_level = fields.Selection([
        ('mat', 'Mật'),
        ('toimat', 'Tối mật'),
        ('tuyetmat', 'Tuyệt mật'),
    ], string='Độ bảo mật')

    page_number = fields.Integer('Số trang')
    language_text = fields.Selection(string='Ngôn ngữ', selection=[('vn', 'Tiếng Việt'), ('eng', 'Tiếng Anh')],  default="vn")

    leadership = fields.One2many(comodel_name="mvb.leadership.direction", inverse_name="text_ids",
                                 string="Bút phê chỉ đạo và xử lý", required=False, )

    # gửi nội bộ công ty

    # member = fields.One2many(comodel_name="mvb.text.go.for.employee", inverse_name="text_go_ids_employee",
    #                          string="Nội bộ",
    #                          required=False)
    member = fields.Many2many(comodel_name="res.users", relation="user_received_text_go", column1="col1", column2="col2",
                                string="Nội bộ")

    # Thông tin lưu trữ
    storage_data = fields.One2many(comodel_name='mvb.document.storage', inverse_name="storage_text_datas",
                                   string="Thông tin lưu trữ",
                                   track_visibility='always')

    is_document = fields.Boolean('Chuyển tới tài liệu dùng chung', default=False)

    # gửi công ty ngoài
    company_external = fields.One2many(comodel_name="mvb.text.go.for.company.external",
                                       inverse_name="text_go_ids_company", string="Đơn vị ngoài",
                                       required=False)
    state_text = fields.Selection(string="Trạng thái văn bản",
                                  selection=[('pending', 'Đang chờ xử lý'), ('finish', 'Kết thúc')],
                                  required=False, )

    file_attachment = fields.Many2many('ir.attachment', 'file_attachment_for_text_go',
                                       'rental_id', 'attachment_id', string="File đính kèm")
    document_ids = fields.One2many(comodel_name="mvb.document",
                                   inverse_name="mvb_text_go_ids", string="Test",
                                   invisiable=True)

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'Số hiệu văn bản đã tồn tại. \n Hãy nhập số hiệu văn bản khác'),
        ('unique_id_text_go', 'unique(id_text_go, text_go_notebook)', 'Số đi văn bản đã tồn tại. \n Hãy nhập số đi văn bản khác'),
    ]

    #onchange dreaft_text_id khi văn thư ấn phát hành văn bản
    @api.onchange('draft_text_id')
    def add_record_from_draft_text_id(self):
        self.name_signed_text = self.draft_text_id.name_signed
        self.job_signed_text = self.draft_text_id.name_signed.mvb_job_name
        self.date_signed_text = self.draft_text_id.date_signed
        self.content_compendium = self.draft_text_id.content_compendium
        self.file_attachment = self.draft_text_id.attachment_ids
        self.user_create = self.draft_text_id.user_create
        self.date_create = self.draft_text_id.date_create
        self.department_create = self.draft_text_id.department_create
        self.job_create = self.draft_text_id.job_create
        self.name = self.draft_text_id.number_text_go

    @api.onchange('text_go_notebook')
    def change_id_text_go(self):
        domain = [('text_go_notebook', 'ilike', self.text_go_notebook.id)]
        res = self.search(domain)
        if res:
            for item in reversed(res):
                if item.id_text_go.isnumeric():
                    self.id_text_go = str(int(item.id_text_go) + 1)
        else:
            self.id_text_go = str(1)

    def change_state_for_draft_text(self):
        domain = [('id', '=', self.draft_text_id.id)]
        res = self.env['mvb.draft.text.go'].search(domain)
        if res:
            res.state = 'finish'
            print(res)
            domain_state_processing = [('name', '=', self.create_uid.id), ('text_ids', '=', self.draft_text_id.id),
                                       ('state', '=', 'chuaxuly')]
            res_status = self.env['mvb.people.processing.textdraft'].search(domain_state_processing)
            print(res_status)
            if res_status:
                for rec in res_status:
                    rec.state = 'daxuly'

    @api.model
    def create(self, vals):
        res = super(MVBTextGo, self).create(vals)
        if res:
            res.change_state_for_draft_text()
        return res

    def save_for_document(self):
        self.state = 'saved'
        list_user = []
        list_user.append(self.env.uid)
        for user in self.member:
            if user:
                list_user.append(user.id)
        vals = {
            'name': self.name,
            'document_type': self.text_go_type.id,
            'name_document': self.content_compendium,
            'date_document': str(self.date_signed_text),
            'document_arrival_date': self.delivery_date,
            'count_document': self.page_number,
            'unit_promulgate': '1',
            'document_notebook': self.text_go_notebook.id,
            'share_user': [(6, 0, list_user)],
        }
        res = self.env['mvb.document'].create(vals)
        rec = self.env['ir.attachment'].search([('res_id', '=', self.id)])
        if rec:
            for item in rec:
                self.env['ir.attachment'].create([{'name': item.name,
                                                   'datas': item.datas,
                                                   'datas_fname': item.name, 'res_model': 'mvb.document',
                                                   'res_id': res.id}])
        if self.file_attachment:
            for word in self.file_attachment:
                self.env['ir.attachment'].create([{'name': word.name,
                                                   'datas': word.datas,
                                                   'datas_fname': word.name, 'res_model': 'mvb.document',
                                                   'res_id': res.id}])

        # form_view_id = self.env.ref('mvb_documents.mvb_document_form_view').id
        # return {
        #     'name': 'Tài liệu cá nhân',
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'mvb.document',
        #     'context': "{'default_mvb_text_go_ids': active_id}",
        #     'view_type': 'form',
        #     'view_mode': 'form',
        #     'view_id': form_view_id,
        #     'target': 'new',
        #     }
    
    @api.onchange('delivery_date')
    def get_document_notebook(self):
        doamin = [("year_doc","=",YEAR_NOW_DEFAULT),("type_doc","=","đi")]
        res = self.env['mvb.document.notebook'].search(doamin)
        self.text_go_notebook = res.id
