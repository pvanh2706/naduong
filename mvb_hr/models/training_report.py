from odoo import api, fields, models, _
import time
from datetime import datetime
from odoo.exceptions import UserError

class TrainReportProperty(models.Model):
    _name = "train.report.property"
    _rec_name = "name"
    _description = "New Description"

    name = fields.Char()
    property_1 = fields.Char("Tiêu chí cấp 1", default="")
    property_2 = fields.Char("Tiêu chí cấp 2", default="")
    property_3 = fields.Char("Tiêu chí cấp 3", default="")
    property_4 = fields.Char("Tiêu chí cấp 4", default="")
    property_5 = fields.Char("Tiêu chí cấp 5", default="")

    label_l1 = fields.Char("Nhãn 1")
    label_l2 = fields.Char("Nhãn 2")
    label_l3 = fields.Char("Nhãn 3")

    amount = fields.Float("Giá trị")
    report_id = fields.Many2one("train.report", "Báo cáo năm", ondelete="cascade")


class TrainReportLine(models.Model):
    _name = "train.report_line"
    _description = "Báo cáo"
    _rec_name = "property_id"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    
    report_id = fields.Many2one("train.report", 
        string="Báo cáo công tác đào tạo, bồi dưỡng năm ",
        required=True,
        readonly=True,
        states={"unlock": [("readonly", False)]},
        track_visibility="onchange", 
        ondelete="cascade")

    property_id = fields.Many2one(
        comodel_name="train.plan.property",
        string="Nội dung đào tạo, bồi dưỡng",
        required=True,
        readonly=True,
        states={"unlock": [("readonly", False)]},
        track_visibility="onchange",
    )
    company_id = fields.Many2one(
        "res.company",
        "Công ty",
        related="property_id.company_id", store = True
    )

    company_amount = fields.Float(
        "Công ty",
        readonly=True,
        states={"unlock": [("readonly", False)]},
        track_visibility="onchange",
    )
    group_amount = fields.Float(
        "Tập đoàn",
        readonly=True,
        states={"unlock": [("readonly", False)]},
        track_visibility="onchange",
    )
    other_amount = fields.Float(
        "Khác",
        readonly=True,
        states={"unlock": [("readonly", False)]},
        track_visibility="onchange",
    )
    attendees_amount = fields.Integer(
        "Dự học",
        readonly=True,
        states={"unlock": [("readonly", False)]},
        track_visibility="onchange",
    )
    qualified = fields.Integer(
        "Đạt yêu cầu",
        readonly=True,
        states={"unlock": [("readonly", False)]},
        track_visibility="onchange",
    )

    state = fields.Selection(
        [("unlock", "Mở"), ("lock", "Khóa"),],
        string="Trạng thái",
        index=True,
        readonly=True,
        copy=False,
        default="unlock",
        track_visibility="onchange",
    )
    sequence = fields.Integer("Thứ tự", related="property_id.sequence",store=True)
    total_amount = fields.Float("Tổng số", readonly=True, compute = "compute_total")
    percent = fields.Float("Tỷ lệ (%)", readonly=True, compute = "compute_percent")
    short_name = fields.Char('Tiêu chí báo cáo', compute='compute_short_name')

    def open_training_report(self):
        return {
            'name': _('Báo cáo công tác đào tạo'),
            'res_id': self.id,
            'view_type': 'form',
            'res_model': 'train.report_line',
            'view_id': False,
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
        }
        
    @api.depends("property_id")
    def compute_short_name(self):
        for em in self:
            em.short_name = em.property_id.short_name

    @api.depends('attendees_amount', 'qualified')
    def compute_percent(self):
        for em in self:
            if em.attendees_amount > 0:
                em.percent = (em.qualified / em.attendees_amount) * 100
            else:
                em.percent = 0

    @api.depends('company_amount', 'group_amount','other_amount')
    def compute_total(self):
        for em in self:
            em.total_amount = em.company_amount + em.group_amount + em.other_amount

class TrainReport(models.Model):
    _name = "train.report"
    _rec_name = "name"
    _description = "Báo cáo năm"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char("Tên", compute="compute_name")
    plan_id = fields.Many2one(
        "train.report.year.plan",
        string="Thuộc kế hoạch",
        required=True,
        ondelete="cascade",
    )
    line_ids = fields.One2many(
        comodel_name="train.report_line",
        inverse_name="report_id",
        string="Báo cáo cho từng nội dung đào tạo, bồi dưỡng",
    )
    # year = fields.Selection([(num, str(num)) for num in range(1999, (datetime.now().year) + 50)], 'Năm',
    #                         default=int((time.strftime('%Y'))), track_visibility='always')
    # _sql_constraints = [
    #     (
    #         "train_report_uniq",
    #         "unique (year)",
    #         "Đã tồn tại báo cáo cho năm này!",
    #     )
    # ]

    def generate_report_line(self):
        if len(self.plan_id.list_property_ids) == 0:
            raise UserError('Bạn cần chọn danh sách tiêu chí trong kế hoạch năm để tạo nhanh cáo cáo')
        list_pro = []
        for line in self.line_ids:
            if line.property_id not in list_pro:
                list_pro.append(line.property_id)

        for line in self.plan_id.list_property_ids:
            if line not in list_pro:
                self.env['train.report_line'].create({
                    'property_id': line.id,
                    'report_id': self.id,
                })


    def lock_data(self):
        list_report = self.env["train.report_line"].search(
            [("report_id", "=", self.id)]
        )
        for line in list_report:
            line.state = "lock"
        return True

    def unlock_data(self):
        list_report = self.env["train.report_line"].search(
            [("report_id", "=", self.id)]
        )
        for line in list_report:
            line.state = "unlock"
        return True

    @api.depends("plan_id")
    def compute_name(self):
        for em in self:
            if em.plan_id.year != False:
                em.name = "Báo cáo công tác đào tạo, bồi dưỡng năm " + str(em.plan_id.year)
            else:
                em.name = "Báo cáo công tác đào tạo, bồi dưỡng"

    @api.model
    def create(self, values):
        # Add code here
        res = super(TrainReport, self).create(values)
        msg = _("Dòng %s được thêm vào báo cáo") % (res.name)
        res.plan_id.message_post(body=msg)
        return res

    @api.multi
    def unlink(self):
        for em in self:
            msg = _("Báo cáo năm %s được <strong>xóa</strong> khỏi kế hoạch") % (
                em.plan_id.year
            )
            em.plan_id.message_post(body=msg)
        return super(TrainReport, self).unlink()

    # hiển thị thông số b/c trên pivot
    # @api.multi
    # def create_report(self):
    #     reports = self.env["train.report.property"].search(
    #         [("report_id", "=", self.id)]
    #     )
    #     reports.unlink()

    #     for line in self.line_ids:
    #         property_1 = ""
    #         property_2 = ""
    #         property_3 = ""
    #         property_4 = ""
    #         property_5 = ""
    #         if len(line.property_id.property_ids) == 1:
    #             property_1 = line.property_id.property_ids[0].name
    #         elif len(line.property_id.property_ids) == 2:
    #             property_1 = line.property_id.property_ids[0].name
    #             property_2 = line.property_id.property_ids[1].name
    #         elif len(line.property_id.property_ids) == 3:
    #             property_1 = line.property_id.property_ids[0].name
    #             property_2 = line.property_id.property_ids[1].name
    #             property_3 = line.property_id.property_ids[2].name
    #         elif len(line.property_id.property_ids) == 4:
    #             property_1 = line.property_id.property_ids[0].name
    #             property_2 = line.property_id.property_ids[1].name
    #             property_3 = line.property_id.property_ids[2].name
    #             property_4 = line.property_id.property_ids[3].name
    #         elif len(line.property_id.property_ids) >= 5:
    #             property_1 = line.property_id.property_ids[0].name
    #             property_2 = line.property_id.property_ids[1].name
    #             property_3 = line.property_id.property_ids[2].name
    #             property_4 = line.property_id.property_ids[3].name
    #             property_5 = line.property_id.property_ids[4].name

    #         self.env["train.report.property"].create(
    #             {
    #                 "property_1": property_1,
    #                 "property_2": property_2,
    #                 "property_3": property_3,
    #                 "property_4": property_4,
    #                 "property_5": property_5,
    #                 "label_l1": "1. Thực hiện năm " + str(self.year),
    #                 "label_l2": "1. Số người",
    #                 "label_l3": "1. Dự học",
    #                 "report_id": self.id,
    #                 "amount": line.attendees_amount,
    #             }
    #         )
    #         self.env["train.report.property"].create(
    #             {
    #                 "property_1": property_1,
    #                 "property_2": property_2,
    #                 "property_3": property_3,
    #                 "property_4": property_4,
    #                 "property_5": property_5,
    #                 "label_l1": "1. Thực hiện năm " + str(self.year),
    #                 "label_l2": "1. Số người",
    #                 "label_l3": "2. Đạt yêu cầu",
    #                 "report_id": self.id,
    #                 "amount": line.qualified,
    #             }
    #         )
    #         for re in self.line_ids:
    #             if re.property_id == line.property_id:
    #                 if re.attendees_amount != 0:
    #                     self.env["train.report.property"].create(
    #                         {
    #                             "property_1": property_1,
    #                             "property_2": property_2,
    #                             "property_3": property_3,
    #                             "property_4": property_4,
    #                             "property_5": property_5,
    #                             "label_l1": "1. Thực hiện năm " + str(self.year),
    #                             "label_l2": "1. Số người",
    #                             "label_l3": "3. Tỷ lệ(%)",
    #                             "report_id": self.id,
    #                             "amount": line.qualified / re.attendees_amount * 100,
    #                         }
    #                     )
    #         self.env["train.report.property"].create(
    #             {
    #                 "property_1": property_1,
    #                 "property_2": property_2,
    #                 "property_3": property_3,
    #                 "property_4": property_4,
    #                 "property_5": property_5,
    #                 "label_l1": "1. Thực hiện năm " + str(self.year),
    #                 "label_l2": "2. Kinh phí(triệu đồng)",
    #                 "label_l3": "1. Công ty",
    #                 "report_id": self.id,
    #                 "amount": line.company_amount,
    #             }
    #         )
    #         self.env["train.report.property"].create(
    #             {
    #                 "property_1": property_1,
    #                 "property_2": property_2,
    #                 "property_3": property_3,
    #                 "property_4": property_4,
    #                 "property_5": property_5,
    #                 "label_l1": "1. Thực hiện năm " + str(self.year),
    #                 "label_l2": "2. Kinh phí(triệu đồng)",
    #                 "label_l3": "2. Tập đoàn",
    #                 "report_id": self.id,
    #                 "amount": line.group_amount,
    #             }
    #         )
    #         self.env["train.report.property"].create(
    #             {
    #                 "property_1": property_1,
    #                 "property_2": property_2,
    #                 "property_3": property_3,
    #                 "property_4": property_4,
    #                 "property_5": property_5,
    #                 "label_l1": "1. Thực hiện năm " + str(self.year),
    #                 "label_l2": "2. Kinh phí(triệu đồng)",
    #                 "label_l3": "3. Khác",
    #                 "report_id": self.id,
    #                 "amount": line.other_amount,
    #             }
    #         )
    #         self.env["train.report.property"].create(
    #             {
    #                 "property_1": property_1,
    #                 "property_2": property_2,
    #                 "property_3": property_3,
    #                 "property_4": property_4,
    #                 "property_5": property_5,
    #                 "label_l1": "1. Thực hiện năm " + str(self.year),
    #                 "label_l2": "2. Kinh phí(triệu đồng)",
    #                 "label_l3": "4. Tổng số",
    #                 "report_id": self.id,
    #                 "amount": line.company_amount
    #                 + line.group_amount
    #                 + line.other_amount,
    #             }
    #         )

        # hiện k/h năm trên pivot

        # for line in self.plan_id.line_ids:
        #     property_1 = ""
        #     property_2 = ""
        #     property_3 = ""
        #     property_4 = ""
        #     property_5 = ""
        #     if len(line.property_id.property_ids) == 1:
        #         property_1 = line.property_id.property_ids[0].name
        #     elif len(line.property_id.property_ids) == 2:
        #         property_1 = line.property_id.property_ids[0].name
        #         property_2 = line.property_id.property_ids[1].name
        #     elif len(line.property_id.property_ids) == 3:
        #         property_1 = line.property_id.property_ids[0].name
        #         property_2 = line.property_id.property_ids[1].name
        #         property_3 = line.property_id.property_ids[2].name
        #     elif len(line.property_id.property_ids) == 4:
        #         property_1 = line.property_id.property_ids[0].name
        #         property_2 = line.property_id.property_ids[1].name
        #         property_3 = line.property_id.property_ids[2].name
        #         property_4 = line.property_id.property_ids[3].name
        #     elif len(line.property_id.property_ids) >= 5:
        #         property_1 = line.property_id.property_ids[0].name
        #         property_2 = line.property_id.property_ids[1].name
        #         property_3 = line.property_id.property_ids[2].name
        #         property_4 = line.property_id.property_ids[3].name
        #         property_5 = line.property_id.property_ids[4].name

        #     self.env["train.report.property"].create(
        #         {
        #             "property_1": property_1,
        #             "property_2": property_2,
        #             "property_3": property_3,
        #             "property_4": property_4,
        #             "property_5": property_5,
        #             "label_l1": "2. Kế hoạch năm tiếp theo",
        #             "label_l2": "1. Số người",
        #             "label_l3": "1. Số người dự học",
        #             "report_id": self.id,
        #             "amount": line.attendees_expected_amount,
        #         }
        #     )

        #     self.env["train.report.property"].create(
        #         {
        #             "property_1": property_1,
        #             "property_2": property_2,
        #             "property_3": property_3,
        #             "property_4": property_4,
        #             "property_5": property_5,
        #             "label_l1": "2. Kế hoạch năm tiếp theo",
        #             "label_l2": "2. Kinh phí(triệu đồng)",
        #             "label_l3": "1. Công ty",
        #             "report_id": self.id,
        #             "amount": line.company_expected_amount,
        #         }
        #     )

        #     self.env["train.report.property"].create(
        #         {
        #             "property_1": property_1,
        #             "property_2": property_2,
        #             "property_3": property_3,
        #             "property_4": property_4,
        #             "property_5": property_5,
        #             "label_l1": "2. Kế hoạch năm tiếp theo",
        #             "label_l2": "2. Kinh phí(triệu đồng)",
        #             "label_l3": "2. Tập đoàn",
        #             "report_id": self.id,
        #             "amount": line.group_expected_amount,
        #         }
        #     )

        #     self.env["train.report.property"].create(
        #         {
        #             "property_1": property_1,
        #             "property_2": property_2,
        #             "property_3": property_3,
        #             "property_4": property_4,
        #             "property_5": property_5,
        #             "label_l1": "2. Kế hoạch năm tiếp theo",
        #             "label_l2": "2. Kinh phí(triệu đồng)",
        #             "label_l3": "3. Khác",
        #             "report_id": self.id,
        #             "amount": line.other_expected_amount,
        #         }
        #     )

        #     self.env["train.report.property"].create(
        #         {
        #             "property_1": property_1,
        #             "property_2": property_2,
        #             "property_3": property_3,
        #             "property_4": property_4,
        #             "property_5": property_5,
        #             "label_l1": "2. Kế hoạch năm tiếp theo",
        #             "label_l2": "2. Kinh phí(triệu đồng)",
        #             "label_l3": "4. Tổng số",
        #             "report_id": self.id,
        #             "amount": line.company_expected_amount
        #             + line.group_expected_amount
        #             + line.other_expected_amount,
        #         }
        #     )

