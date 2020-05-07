from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class DocumentBiddingState(models.Model):
    _name = 'mvb.document.biddingstate'
    _description = 'Danh mục các giai đoạn gói thầu'
    _rec_name = 'id_bidding_state'

    id_bidding_state = fields.Many2one(comodel_name='mvb.document.bidding.package', string='Tên gói thầu',
                                       track_visibility='onchange', ondelete="cascade",)

    state_bidding = fields.Selection([
        ('giaidoan_1', 'Chuẩn bị lựa chọn nhà thầu'),
        ('giaidoan_2', 'Tổ chức lựa chọn nhà thầu'),
        ('giaidoan_3', 'Đánh giá hồ sơ'),
        ('giaidoan_4', 'Trình, thẩm định, phê duyệt và công khai kết quả'),
        ('giaidoan_5', 'Đàm phán, hoàn thiện, ký kết hợp đồng'),
        ('giaidoan_6', 'Thực hiện hợp đồng'),
    ], string="Giai đoạn", default='giaidoan_1')

    bidding_packages_list = fields.Many2one(comodel_name='mvb.document', string='Số hiệu tài liệu', ondelete="cascade", readonly= True)
    name_document_bidding = fields.Text(string="Tên tài liệu", compute='_compute_field', readonly=True)
    project_name = fields.Char('Tên dự án',readonly=True)
    document_type = fields.Char(string="Loại tài liệu",compute='_compute_field', readonly=True)
    date_document = fields.Date(string="Ngày tài liệu", compute='_compute_field',readonly =True)


    @api.one
    @api.depends('bidding_packages_list')
    def _compute_field(self):
        """
        @api.depends() should contain all fields that will be used in the calculations.
        """
        self.document_type = self.bidding_packages_list.document_type.name
        self.name_document_bidding = self.bidding_packages_list.name_document
        self.date_document = self.bidding_packages_list.date_document

    @api.multi
    @api.constrains('id_bidding_state')
    def validate_bidding(self):
        if len(self.id_bidding_state) == 0:
            raise ValidationError(_("Bạn cần lựa chọn loại gói thầu"))
        else:
            if len(self.id_bidding_state.bidding_code) == 0:
                raise ValidationError(_("Bạn cần tạo tên gói thầu"))

    @api.model
    def create(self, vals):
        if vals.get('id_bidding_state'):
            id_bidding = int(vals.get('id_bidding_state'))
            project_name = self.env['mvb.document.bidding.package'].browse(id_bidding).project_id.name
            if project_name:
                vals.update({'project_name': project_name})
        res = super(DocumentBiddingState, self).create(vals)
        msg = ''
        if res.id_bidding_state.name:
            msg = msg + ('<li>Gói thầu: %s </li>') % res.id_bidding_state.name
        if res.id_bidding_state.project_id.name:
            msg = msg + ('<li>Tên dự án: %s </li>') % res.id_bidding_state.project_id.name + '\n'
        if res.state_bidding:
            msg = msg + ('<li> Giai đoạn: %s </li>') % (
                dict(res._fields['state_bidding'].selection).get(res.state_bidding))
        if msg != '':
            new_msg = ('<p>Thêm mới:</p>')
            new_msg = new_msg + msg
            res.bidding_packages_list.message_post(body=new_msg)
        return res

    @api.model
    def write(self, vals):
        is_update_bidding = False
        is_update_bidding_state = False
        if vals.get('id_bidding_state'):
            is_update_bidding = True
        if vals.get('state_bidding'):
            is_update_bidding_state = True
        msg = ''
        # if self.id_bidding_state:
        #     if self.id_bidding_state.project_id:
        #         vals.update({'project_name': self.id_bidding_state.project_id.name})
        res = super(DocumentBiddingState, self).write(vals)
        if is_update_bidding == True:
            msg = msg + ('<li>Cập nhật gói thầu: %s</li>') % (self.id_bidding_state.name)
        if self.id_bidding_state.project_id.name and is_update_bidding == True:
            msg = msg + ('<li>Dự án: %s</li>') % (self.id_bidding_state.project_id.name)
        if is_update_bidding_state == True:
            if is_update_bidding == False:
                msg = msg + ('<li>Gói thầu: %s</li>') % (self.id_bidding_state.name)
            msg = msg + ('<li> Giai đoạn: %s </li>') % (
                dict(self._fields['state_bidding'].selection).get(self.state_bidding))
        if msg != '':
            new_msg = ('<p>Cập nhật:</p>') + msg
            self.bidding_packages_list.message_post(body=new_msg)
        return res

    @api.model
    def unlink(self):
        name_package = self.id_bidding_state.name
        msg = ('<p>Xóa gói thầu: %s</p>'
               '<ul>'
               '<li> Giai đoạn: %s </li>'
               '</ul>') % (name_package, dict(self._fields['state_bidding'].selection).get(self.state_bidding))
        self.bidding_packages_list.message_post(body=msg)
        res = super(DocumentBiddingState, self).unlink()
        return res

    @api.onchange('id_bidding_state')
    def onchange_method(self):
        if self:
            self.project_name = self.id_bidding_state.project_id.name
