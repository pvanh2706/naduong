from odoo import api, fields, models
import time
from odoo.exceptions import UserError, ValidationError, Warning
from odoo.osv import osv
from odoo.tools.translate import _
from datetime import datetime, timedelta

class MVBDocumentPublisher(models.Model):
    _name = 'mvb.document.publisher'
    _rec_name = 'name'
    _description = 'Đơn vị phát hành'

    name = fields.Char('Tên')
    note = fields.Text(string='Ghi chú')


    @api.model
    def create(self, values):
        # Add code here
        return super(MVBDocumentPublisher, self).create(values)


class DocumentMVB(models.Model):
    _name = 'mvb.document'
    _description = 'Tài liệu'
    _inherit = ['mail.activity.mixin', 'mail.thread']

    name = fields.Char('Số hiệu tài liệu', track_visibility='onchange')
    document_type = fields.Many2one(comodel_name='mvb.document.type', string='Loại tài liệu',
                                    track_visibility='onchange', ondelete="cascade")

    name_document = fields.Text('Tên tài liệu', track_visibility='onchange')
    date_document = fields.Date('Ngày của tài liệu', track_visibility='onchange')
    date_update = fields.Date('Ngày cập nhật', track_visibility='onchange')
    people_update = fields.Char('Người cập nhật', track_visibility='onchange', default=lambda self: self.env.user.name)

    count_document = fields.Integer('Số trang', track_visibility='onchange')
    bidding_packages_list = fields.One2many(comodel_name="mvb.document.biddingstate",
                                            inverse_name="bidding_packages_list", string="Gói thầu", required=False,
                                            track_visibility='onchange', )
    share_user = fields.Many2many(comodel_name="res.users", relation="mvb_document_share_user_rel",
                                  string="Chia sẻ tài liệu", track_visibility='onchange',
                                  default=lambda self: self.env.user, store=True)

    storage_data = fields.One2many(comodel_name='mvb.document.storage', inverse_name="storage_datas", string="Lưu trữ", track_visibility='always')

    rent_ids = fields.One2many(comodel_name="mvb.document.rent", inverse_name="rent_ids",
                               string="Danh sách lấy tài liệu", required=False, track_visibility='onchange')
    state_document = fields.Selection([('public_state', 'Dùng chung'), ('private_state', 'Dùng riêng')],
                                      string='Trạng thái tài liệu', )
    add_remove_multi_user = fields.Selection([('none_action','Không thực hiện'),('add_all_user', 'Thêm tất cả người dùng'),('remove_all_user','Gỡ tất cả người dùng'),],  string="Thêm/Xóa", default='none_action')

    # add values of contract
    type_contract_document = fields.Many2one(comodel_name="mvb.document.contract.type", string="Loại hợp đồng", required=False, track_visibility='onchange')
    date_contract = fields.Date('Ngày tháng hợp đồng', track_visibility='onchange')
    unit_signing = fields.Char('Đơn vị kí kết', track_visibility='onchange')
    payment_term = fields.Date('Hạn', track_visibility='onchange')
    tl = fields.Char('Thanh lý hợp đồng', track_visibility='onchange')
    unit_contract = fields.Char('Đơn vị tính', track_visibility='onchange')

    contract_values_quantity = fields.Float('Sản lượng', track_visibility='onchange')
    contract_values_cost = fields.Float('Giá trị (đồng)', digits=(16, 2), track_visibility='onchange')

    contract_values_action_quantity = fields.Float('Sản lượng' ,track_visibility='onchange')
    contract_values_action_cost = fields.Float('Giá trị (đồng)', digits=(16,2), track_visibility='onchange')

    start_contract = fields.Date('Thời gian bắt đầu', track_visibility='onchange')
    end_contract = fields.Date('Thời gian kết thúc', track_visibility='onchange')

    liquidation = fields.Char('Thanh lý', track_visibility='onchange')
    note_contract = fields.Text('Ghi chú', track_visibility='onchange' )

    # property hire contract

    hire_location_pay = fields.Char('Vị trí', track_visibility='onchange')
    hire_contract_amount = fields.Float('Sản lượng', track_visibility='onchange')
    hire_contract_values = fields.Float('Giá trị', track_visibility='onchange')
    q = fields.Char('Q', track_visibility='onchange')
    hire_contract_number = fields.Integer('Số lượng', track_visibility='onchange')

    unit_promulgate = fields.Many2one('mvb.document.publisher',string= 'Đơn vị ban hành', track_visibility='onchange')
    document_arrival_date = fields.Date('Ngày đến tài liệu', track_visibility='onchange')
    has_attachment = fields.Boolean(string='Có đính kèm?', compute='compute_has_attachment')

    document_notebook = fields.Many2one(comodel_name="mvb.document.notebook", string="Sổ văn bản", required=False, track_visibility='onchange' )

    # project_not_bidding = fields.Many2one(comodel_name="mvb.document.project", string="Dự án không có gói thầu", domain=[('is_have_bidding', '=', True)], required=False, )
    is_not_bidding = fields.Boolean('Có/Không?', default=False)
    project_not_bidding = fields.Many2one(comodel_name="mvb.document.project", string="Tên dự án", required=False, )
    project_name = fields.Char(string='Tên dự án')
    # Đóng mở tài liệu
    active_lock = fields.Boolean(string="Check Lock", default=True)


    @api.onchange('is_not_bidding')
    def onchange_name(self):
        if self:
            self.project_not_bidding = []


    def get_email_to(self):
        return self.create_uid.email

    def send_email(self, emp_id, template_xml_id):
        if template_xml_id:
            mail_template = self.env.ref(
                'mvb_documents.%s' % (template_xml_id))
            if mail_template:
                mail_template.send_mail(
                    emp_id, force_send=True, raise_exception=False)
        return True

    @api.multi
    @api.returns('mail.message', lambda value: value.id)
    def message_post_notification(self, **kwargs):
        return super(DocumentMVB, self.with_context(mail_post_autofollow=False)).message_post(**kwargs)

    def cron_check_contract_end_date(self):
        next_7_days = (fields.Date.from_string(fields.Date.today()) + timedelta(days=7)).strftime("%Y-%m-%d")

        emp_records = self.search([('end_contract', 'in', [next_7_days])])

        for em in emp_records:
            list_partner_id = []
            for user in em.share_user:
                list_partner_id.append(user.partner_id.id)
            msg = "Tài liệu " +  em.name + " sắp đến hạn kết thúc hợp đồng!"
            em.message_post(body=msg, partner_ids=list_partner_id)
        return True


    def compute_has_attachment(self):
        for em in self:
            attachments = self.env['ir.attachment'].search([('res_model', '=', 'mvb.document'), ('res_id', '=', em.id)])
            if len(attachments) > 0:
                em.has_attachment = True
            else:
                em.has_attachment = False


    @api.constrains('start_contract', 'end_contract')
    def _check_dates(self):
        if self.start_contract and self.end_contract:
            if self.filtered(lambda c: c.end_contract and c.start_contract > c.end_contract):
                raise ValidationError(_('Thời gian bắt đầu hợp đồng phải nhỏ hơn ngày kết thúc hợp đồng'))

    @api.onchange('add_remove_multi_user')
    def document_add_all_user_test(self):
        data_document = self._origin
        if self.add_remove_multi_user == 'add_all_user':
            user_document = self.env['res.users'].search([])
            self.share_user = user_document
        elif self.add_remove_multi_user == 'remove_all_user':
            user_document = []
            if self._uid != self._origin.create_uid.id:
                raise ValidationError(_('Chỉ có người tạo văn bản mới sử dụng được chức năng này!'))
            else:
                if self._origin:
                    user_document = self.env['res.users'].search([('id', '=', self.env.user.id), ('id', '=', self._origin.create_uid.id)])
                else:
                    user_document = self.env['res.users'].search([('id', '=', self.env.user.id)])
                self.share_user = user_document


    @api.onchange('document_type')
    def _get_number_code1(self):
        if self.document_type:
            if self.document_type.no_number_document == True:
                suffixes_code = self.document_type.suffixes
                if suffixes_code == False:
                   suffixes_code = ''
                number_code = 1
                new_name = str(number_code).zfill(4) + suffixes_code
                document_current = self.env['mvb.document'].search([])
                code_number_ok = False
                while code_number_ok == False:
                    if document_current:
                        for rec in document_current:
                            if new_name == rec.name:
                                number_code = number_code + 1
                                new_name = str(number_code).zfill(4) + suffixes_code
                                code_number_ok = False
                                break;
                            else:
                                code_number_ok = True
                    else:
                        code_number_ok = True
                self.name = new_name

    @api.onchange('share_user')
    def check_share_user(self):
        if self.env.user not in self.share_user:
            raise UserError('Bạn không thể xóa user hiện tại')
        if self._origin.create_uid:
            if self._origin.create_uid not in self.share_user :
                raise UserError('Bạn không thể xóa người tạo tài liệu')

    @api.multi
    @api.constrains('name', 'document_type', 'date_document' , 'count_document','bidding_packages_list')
    def update_people(self):
        if len(self.document_type) == 0:
            raise ValidationError(_("Bạn cần lựa chọn loại tài liệu"))
        if self.name == False:
            raise ValidationError(_('Bạn cần điền số hiệu tài liệu'))
        # if self.name_document == False:
        #     raise ValidationError(_('Bạn cần nhập tên tài liệu'))
        # Update user update
        for rec in self:
            if(rec.people_update != self.env.user.name):
                rec.people_update = self.env.user.name

    @api.multi
    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        return super(DocumentMVB, self.with_context(mail_post_autofollow=True)).message_post(**kwargs)

    @api.model
    def create(self, values):
        # check
        print(values.get('active_lock'))
        if values.get('active_lock'):
            values.update({'active_lock': False})
        curent_self = self
        if values.get('is_not_bidding') == True:
            if values.get('project_not_bidding'):
                name = self.env['mvb.document.project'].browse(int(values.get('project_not_bidding'))).name
                values.update({'project_name': name})
        current_document = self.env['mvb.document'].sudo().search([])
        strName = ''
        strDate = 'False'
        if values.get('name'):
            strName = values.get('name').strip()
        if values.get('date_document'):
            strDate = values.get('date_document').strip()
        new_number_name = strName + strDate
        for rec in current_document:
            if new_number_name == (str(rec.name).strip() + str(rec.date_document).strip()):
                name_login = rec.create_uid.login
                name_user = rec.create_uid.name
                msg = ('Số hiệu tài liệu phải là duy nhất! (Số hiệu tài liệu bao gồm: Tên số hiệu + ngày tài liệu )\n'
                       ' Tài liệu này đã được tài khoản khác tạo trước:\n '
                       '- Tên người dùng: %s \n'
                       '- Tên tài khoản: %s') % (name_user, name_login)
                raise osv.except_osv(_('Lỗi số hiệu tài liệu'), _(msg))
        values.update({'add_remove_multi_user': 'none_action'})

        # Kiểm tra thông tin việc tạo văn bản từ phía eGOV
        if values.get('eGov') == 'True':
            if values.get('create_by'):
                search_id_create_user = self.env['res.users'].search([('login', '=', values.get('create_by'))],
                                                                     limit=1).id
                if search_id_create_user:
                    curent_self = self.env['mvb.document'].with_env(self.env(user=search_id_create_user))
                    print('ttt')
        res = super(DocumentMVB, curent_self).create(values)
        if len(res.share_user) > 1:
            res.state_document = 'public_state'
        elif len(res.share_user) == 1:
            res.state_document = 'private_state'
        res.add_remove_multi_user = 'none_action'
        msg = '<li>Người được chia sẻ:<li>'
        for user in res.share_user:
            if self.env.user != user:
                msg = msg + ('<li>Người dùng: %s</li>') % (user.name)
        if msg != '':
            res.message_post(body=msg)
        return res
    # @api.multi
    # def write(self, values):
    #     # Add code here
    #     return super(ClassName, self).write(values)

    @api.multi
    def write(self, values):
        # validate name
        if values.get('is_not_bidding') == True or values.get('project_not_bidding'):
            if values.get('project_not_bidding'):
                name = self.env['mvb.document.project'].browse(int(values.get('project_not_bidding'))).name
                values.update({'project_name': name})

        if values.get('name'):
            current_document = self.env['mvb.document'].sudo().search([])
            for rec in current_document:
                if str(values.get('name')).strip() == str(rec.name).strip():
                    name_login = rec.create_uid.login
                    name_user = rec.create_uid.name
                    msg = ('Số hiệu tài liệu phải là duy nhất! Tài liệu này đã được tài khoản khác tạo trước:\n '
                           '- Tên người dùng: %s \n'
                           '- Tên tài khoản: %s') % (name_user, name_login)
                    raise osv.except_osv(_('Lỗi số hiệu tài liệu'), _(msg))

        old_self = self.share_user

        if values.get('share_user') != None:
            a = str(values.get('share_user')).split('[')[3]
            b = a.split(']]')[0].replace(" ", "")
            n = b.split(',')
            if len(n) > 1:
                self.state_document = 'public_state'
            elif len(n) == 1:
                self.state_document = 'private_state'
        values.update({'add_remove_multi_user': 'none_action'})

        # Kiểm tra thông tin việc tạo văn bản từ phía eGOV
        if values.get('eGov') == 'True':
            if values.get('create_by'):
                search_id_create_user = self.env['res.users'].search([('login', '=', values.get('create_by'))],
                                                                     limit=1).id
                if search_id_create_user:
                    curent_self = self.env['mvb.document'].with_env(self.env(user=search_id_create_user))

        res = super(DocumentMVB, self).write(values)
        new_self = self.share_user
        array_add = []
        array_delete = []

        ids_old_self = old_self.ids
        ids_new_self = new_self.ids

        for i in ids_old_self:
            if i not in ids_new_self:
                array_delete.append(i)
        for j in ids_new_self:
            if j not in ids_old_self:
                array_add.append(j)
        msg = ''
        if len(array_add) > 0 or len(array_delete) > 0:
            msg = msg + ('<p>Cập nhật danh sách chia sẻ tài liệu:</p>')
        if len(array_add) > 0:
            msg = msg + ('<ul>Danh sách thêm người xem:')
            for n in array_add:
                msg = msg + ('<li>Người dùng: %s</li>') % new_self.browse(int(n)).name

            msg = msg + '</ul>'
        if len(array_delete) > 0:
            msg = msg + ('<ul>Danh sách xóa người xem:')
            for m in array_delete:
                msg = msg + ('<li>Người dùng: %s</li>') % old_self.browse(int(m)).name

            msg = msg + '</ul>'
        if msg != '':
            self.message_post(body=msg)
        return res

    @api.multi
    def unlink(self):
        # Add code here
        for rec in self:
            if rec.state_document == 'public_state':
                raise osv.except_osv(_('Lỗi xóa tài liệu'), _('Bạn không thể xóa tài liệu dùng chung.\n Vui lòng chuyển về tại liệu cá nhân trước khi xóa!'))
            # if rec.name:
            #     document_type = rec.document_type
            #     for t in document_type.code_number:
            #         if t.name == rec.name:
            #             t.unlink()
        return super(DocumentMVB, self).unlink()

    @api.multi
    def action_download_attachment(self):
        tab_id = []
        for rec in self:
            attachments = self.env['ir.attachment'].search(
                [('res_model', '=', 'mvb.document'), ('res_id', '=', rec.id)])
            for attachment in attachments:
                tab_id.append(attachment.id)
            msg = "Tất cả file đính kèm đã được <strong>Tải xuống</strong>!"
            rec.message_post(body=msg)

        url = '/web/binary/download_document?tab_id=%s' % tab_id
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'self',
        }



    @api.multi
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        if ('name' not in default):
            default['name'] = _("%s (copy)") % self.name
        return super(DocumentMVB, self).copy(default)

    def open_line(self):
        test = 100
        return {
                'name': _('Tài liệu dùng chung'),
                'res_id': self.id,
                'view_type': 'form',
                'res_model': self._name,
                'view_id': False,
                'view_mode': 'form',
                'type': 'ir.actions.act_window',
                'target': 'current'
        }



