from odoo import api, fields, models,_
import time
from datetime import datetime
from odoo.exceptions import UserError

class DisciplineSubProperty(models.Model):
    _name = 'discipline.sub.property'
    _rec_name = 'name'
    _description = 'New Description'
    _order = 'level'

    name = fields.Char('Tên')
    level = fields.Integer('Cấp độ')
    sequence = fields.Integer('Thứ tự')

class DisciplineProperty(models.Model):
    _name = 'discipline.property'
    _rec_name = 'name'

    name = fields.Char('Tên', compute='_compute_name', store=True)
    sequence = fields.Integer('Thứ tự')
    company_id = fields.Many2one(
        "res.company", string="Công ty"
    )
    property_ids = fields.Many2many(comodel_name="discipline.sub.property", string="Chức danh bị xử lý kỷ luật")
    
    @api.depends('property_ids.name')
    def _compute_name(self):
        for em in self:
            em.name = ""
            for line in em.property_ids:
                em.name = str(em.name) + "[" + str(line.name) + "]"

class DisciplineReport(models.Model):
    _name = 'discipline.report'
    _rec_name = 'name'
    _description = 'Báo cáo năm'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char('Tên', compute='compute_name')
    year = fields.Selection([(num, str(num)) for num in range(1999, (datetime.now().year) + 50)], 'Năm',
                             default=int((time.strftime('%Y'))), track_visibility='always')
    list_property_ids = fields.Many2many('discipline.property', string='Danh sách tiêu chí')
    line_ids = fields.One2many(
    comodel_name="discipline.report_line",
    inverse_name="report_id",
    string="Báo cáo của đơn vị",
    )

    @api.depends('year')
    def compute_name(self):
        for em in self:
            em.name = "Báo cáo xử lý kỷ luật cán bộ " + "năm " + str(
                em.year)

    def generate_report_line(self):
        if len(self.list_property_ids) == 0:
            raise UserError('Bạn cần chọn danh sách tiêu chí để tạo báo cáo')
        list_pro = []

        for line in self.list_property_ids:
            if line not in list_pro:
                self.env['discipline.report_line'].create({
                    'report_id' : self.id,
                    'property_id': line.id,
                })


    def lock_data(self):
        list_report = self.env["discipline.report_line"].search(
            [("report_id", "=", self.id)]
        )
        for line in list_report:
            line.state = "lock"
        return True

    def unlock_data(self):
        list_report = self.env["discipline.report_line"].search(
            [("report_id", "=", self.id)]
        )
        for line in list_report:
            line.state = "unlock"
        return True

    @api.multi
    @api.returns("mail.message", lambda value: value.id)
    def message_post(self, **kwargs):
        return super(
            DisciplineReport, self.with_context(mail_post_autofollow=True)
        ).message_post(**kwargs)


class DisciplineReportLine(models.Model):
    _name = 'discipline.report_line'
    _rec_name = 'property_id'
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char('Tên', compute='compute_name')
    property_id = fields.Many2one(comodel_name="discipline.property", string="Tiêu chí", required=True)
    report_id = fields.Many2one('discipline.report', string='Báo cáo năm', required=True, ondelete="cascade")

    total = fields.Integer('Tổng số')
    in_period_communist_mem = fields.Integer('Đảng viên')
    in_period_women = fields.Integer('Phụ nữ')
    discipline_reason = fields.Text('Lý do bị xử lý kỷ luật')

    kld_khientrach = fields.Integer('Khiển trách')
    kld_canhcao = fields.Integer('Cảnh cáo')
    kld_cachchuc = fields.Integer('Cách chức')
    kld_luudang = fields.Integer('Lưu Đảng')
    kld_khaitru = fields.Integer('Khai trừ')

    lld_khientrach = fields.Integer('Khiển trách')
    lld_keodai = fields.Integer('Kéo dài thời hạn nâng lương')
    lld_chuyenviec = fields.Integer('Chuyển việc khác, hạ lương')
    lld_khaitru = fields.Integer('Cách chức')
    lld_sathai = fields.Integer('Sa thải')

    lcb_khientrach = fields.Integer('Khiển trách')
    lcb_canhcao = fields.Integer('Cảnh cáo')
    lcb_haluong = fields.Integer('Hạ lương')
    lcb_hangach = fields.Integer('Hạ ngạch')
    lcb_cachchuc = fields.Integer('Cách chức')
    lcb_thoiviec = fields.Integer('Buộc thôi việc')

    lhs_caitao = fields.Integer('Cải tạo')
    lhs_quanche = fields.Integer('Quản chế')
    lhs_tutreo = fields.Integer('Tự treo')
    lhs_tugiam = fields.Integer('Tự giam')
    lhs_tuhinh = fields.Integer('Tử hình')

    property_id = fields.Many2one(
        comodel_name="discipline.property",
        string="Tiêu chí",
        required=True,
        track_visibility="onchange",
        readonly=True,
        states={"unlock": [("readonly", False)]},
    )
    sequence = fields.Integer('Thứ tự', related="property_id.sequence", store=True)
    company_id = fields.Many2one(
        "res.company",
        "Công ty",
        related="property_id.company_id",
    )
    report_id = fields.Many2one(
        "discipline.report",
        string="Báo cáo tháng",
        required=True,
        ondelete="cascade",
        track_visibility="onchange",
    )

    state = fields.Selection(
        [("unlock", "Mở"), ("lock", "Khóa"),],
        string="Trạng thái",
        index=True,
        readonly=True,
        copy=False,
        default="unlock",
    )

    @api.model
    def create(self, values):
        # Add code here
        res = super(DisciplineReportLine, self).create(values)
        msg = _("Dòng %s được thêm vào báo cáo") % (res.property_id.name)
        res.report_id.message_post(body=msg)
        return res

    @api.multi
    def unlink(self):
        for em in self:
            msg = _("Dòng %s được <strong>xóa</strong> khỏi báo cáo") % (
                em.property_id.name
            )
            em.report_id.message_post(body=msg)
        return super(DisciplineReportLine, self).unlink()