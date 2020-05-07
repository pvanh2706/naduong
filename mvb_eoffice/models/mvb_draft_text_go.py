from odoo import api, fields, models, _
from odoo.osv import expression
from datetime import datetime
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError
from odoo import tools
# import base64
# import docx2txt
# import mammoth
# import html


# from odoo import tools
class MVBPeopleProcessingTextDraft(models.Model):
    _name = 'mvb.people.processing.textdraft'
    _description = 'Tình trạng công việc nhân viên theo văn bản dự thảo  '
    _order = "text_ids desc"

    text_ids = fields.Many2one(comodel_name="mvb.draft.text.go", string="Văn bản", required=False, ondelete='cascade')
    name = fields.Many2one(comodel_name="res.users", string="Người xử lý", )
    state = fields.Selection(string="Tình trạng", selection=[('chuaxuly', 'Chưa xử lý'), ('daxuly', 'Đã xử lý'),
                                                             ('dapheduyet', 'Đã phê duyệt')],
                             required=False, )
    notes = fields.Text('Nội dung')
    name_send = fields.Many2one(comodel_name="res.users", string="Người gửi", )
    department_name_send = fields.Char('Phòng ban', related="name_send.mvb_department_name", store=True)
    date_received = fields.Datetime(string='Ngày Nhận', default=fields.Datetime.now)
    date_view = fields.Datetime(string='Ngày đọc văn bản')
    check_unit = fields.Boolean(string='Check đã xem', default=True)
    dead_line = fields.Datetime(string="Thời hạn xử lý", required=False)

    def btn_textdraft(self):
        if self:
            # if self.check_unit == True:
            self.date_view = tools.datetime.now()
            # self.check_unit = False
            return {
                'name': _('Văn bản dự thảo'),
                'res_id': self.text_ids.id,
                'view_type': 'form',
                'res_model': 'mvb.draft.text.go',
                'view_id': False,
                'view_mode': 'form',
                'type': 'ir.actions.act_window',
            }

    def document_go_warning_deadline_cron_job(self):
        document_now = datetime.now()
        res = self.env['mvb.people.processing.textdraft'].search(
            [('state', '=', 'chuaxuly'), ('dead_line', '<', document_now)])
        if res:
            for record in res:
                list_user_ids = [record.name.id]
                # gui thong bao
                msg = 'Thông báo hạn xử lý đã hết với văn bản: ' + record.text_ids.number_text_go + '</br>' + 'Trích yếu nội dung: ' + str(
                    record.text_ids.content_compendium)
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


class MVBProcessingTextDraft(models.Model):
    _name = 'mvb.processing.textdraft'
    _description = 'Quản lý theo dõi tình trạng của văn bản dự thảo'
    _order = "textdraft_ids desc"

    textdraft_ids = fields.Many2one(comodel_name="mvb.draft.text.go", string="Văn bản",
                                    required=False, ondelete='cascade')
    user_received = fields.Many2many(comodel_name="res.users", relation="people_received",
                                     column1="column1", column2="column2", string="Người nhận")
    notes = fields.Text('Nội dung')
    user_send = fields.Many2one(comodel_name="res.users", string="Người gửi", )
    date = fields.Datetime(string='Ngày gửi', default=fields.Datetime.now)


class CreateDraftText(models.Model):
    _name = 'mvb.draft.text.go'
    _description = 'Tạo văn bản dự thảo'
    _rec_name = "name_seq"
    _order = "name_seq desc"

    # def _default_content(self):
    #     my_string = "Toàn"
    # #
    #     return my_string

    content_compendium = fields.Text(string='Trích yếu nội dung (*)', track_visibility='onchange', required=True)

    attachment_ids = fields.Many2many('ir.attachment', 'car_rent_checklist_ir_attachments_rel',
                                      'rental_id', 'attachment_id', string="File đính kèm")
    document_draft = fields.Html(string="Soạn văn bản", )
    state = fields.Selection(string="Trạng thái văn bản",
                             selection=[('draft', 'Tạo văn bản dự thảo'), ('pending_leader', 'Chờ phê duyệt'),
                                        ('confirm', 'Đã phê duyệt'), ('sending', 'Văn thư chuyển văn bản'),
                                        ('finish', 'Kết thúc')],
                             required=False, default='draft')
    incoming_text_id = fields.Many2many(comodel_name='mvb.incoming.text', relation="reply_incoming_text",
                                        column1="col1", column2="col2", string='Trả lời cho văn bản đến')

    status_text = fields.One2many(string='Tình trạng công việc', comodel_name="mvb.people.processing.textdraft",
                                  inverse_name="text_ids",
                                  required=False, )
    status_line = fields.One2many(string='Theo dõi văn bản', comodel_name="mvb.processing.textdraft",
                                  inverse_name="textdraft_ids",
                                  required=False, )
    number_text_go = fields.Char('Số hiệu văn bản')
    name_seq = fields.Char(string='Mã văn bản dự thảo', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('Tạo văn bản dự thảo'))
    name_signed = fields.Many2one(comodel_name="res.users")
    date_signed = fields.Date('Ngày ký')
    user_create = fields.Many2one(comodel_name="res.users", string="Người tạo văn bản")
    check_user_create = fields.Boolean(string="Kiem tra", default=True)
    date_create = fields.Date('Ngày tạo')
    department_create = fields.Char('Phòng ban', related="user_create.mvb_department_name", store=True)
    job_create = fields.Char('Chức vụ', related="user_create.mvb_department_name", store=True)

    # @api.onchange('attachment_ids', 'number_text_go')
    # def get_data_document(self):
    #     base64_img_bytes = self.attachment_ids.datas
    #     if base64_img_bytes:
    #         with open('document.docx', 'wb') as file_to_save:
    #             base64_encoded_data = base64.decodebytes(base64_img_bytes)
    #             file_to_save.write(base64_encoded_data)
    #             file_to_save.close()
    #         my_text = docx2txt.process("document.docx")
    #         f = open("document.docx", 'rb')
    #         document = mammoth.convert_to_html(f)
    #         html = document.value
    #         print(html)
    #         for word in html:
    #             print(word)
    #         self.document_draft ='<div class="container" style="font-family:Times New Roman; font-size: 13px; ">%s</div>' % (
    #             html)

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('mvb.draft.text.go.sequence') or _('New')
        result = super(CreateDraftText, self).create(vals)
        return result

    def waitting_send_draft_text(self):
        if self:
            form_view_id = self.env.ref('mvb_eoffice.mvb_text_draft_wizard_form').id
            return {
                'name': 'Xử lý văn bản dự thảo',
                'type': 'ir.actions.act_window',
                'res_model': 'mvb.text.draft.wizard',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': form_view_id,
                'target': 'new',
            }

    def comfirm_text(self):
        if self:
            form_view_id = self.env.ref('mvb_eoffice.mvb_text_draft_confirm_wizard_form').id
            return {
                'name': 'Bút phê chỉ đạo',
                'type': 'ir.actions.act_window',
                'res_model': 'mvb.text.draft.wizard',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': form_view_id,
                'context': {'default_name_ids': self.get_id_vt()},
                'target': 'new',
            }
    def get_id_vt(self):
        if self:
            list_user = []
            res = self.env['res.users'].search([("mvb_job_name","=","Văn thư")])
            for user in res:
                list_user.append(user.id)

            form_view_id = self.env.ref('mvb_eoffice.mvb_text_draft_confirm_wizard_form1').id
            list_user.append(self.create_uid.id)
            # for item in self.status_text:
            #     if item.name.id != self.env.uid:
            #         list_user.append(item.name.id)
            data_test = self.env['res.users'].search_read([("mvb_job_name","=","Văn thư")])
            
            for items in data_test:
                for key, value in items:
                    print(key)
            return [(6,0,list_user)]


    def reject_text(self):
        if self:
            form_view_id = self.env.ref('mvb_eoffice.mvb_text_draft_confirm_wizard_form1').id
            list_user_send = []
            list_user_send.append(self.create_uid.id)
            for item in self.status_text:
                if item.name.id != self.env.uid:
                    list_user_send.append(item.name.id)
            return {
                'name': 'Bút phê chỉ đạo',
                'type': 'ir.actions.act_window',
                'res_model': 'mvb.text.draft.wizard',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': form_view_id,
                'context': {'default_name_ids': [(6,0,list_user_send)]},
                'target': 'new',
            }

    def create_text_go(self):
        if self:
            self.state = 'sending'
            form_view_id = self.env.ref('mvb_eoffice.mvb_text_go_form_view').id
            return {
                'name': 'Văn bản đi',
                'type': 'ir.actions.act_window',
                'res_model': 'mvb.text.go',
                'context': "{'default_draft_text_id': active_id}",
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': form_view_id,
                'target': 'new',
            }
