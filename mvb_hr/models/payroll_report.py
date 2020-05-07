from odoo import api, fields, models, _
import time
from datetime import datetime
from odoo.exceptions import UserError
import time
import datetime as dt


class PayrollReportProperty(models.Model):
    _name = "payroll.report.property"
    _rec_name = "name"
    _description = "New Description"

    name = fields.Char()
    property_1 = fields.Char('Tiêu chí cấp 1', default='')
    property_2 = fields.Char('Tiêu chí cấp 2', default='')
    property_3 = fields.Char('Tiêu chí cấp 3', default='')

    label_l1 = fields.Char('Nhãn 1')
    label_l2 = fields.Char('Nhãn 2')
    amount = fields.Float('Giá trị')
    report_id = fields.Many2one('payroll.report', 'Báo cáo tháng', ondelete="cascade")


# B/c cua cac d/vi
class PayrollReportLine(models.Model):
    _name = "payroll.report_line"
    _description = "Báo cáo tháng của các đơn vị"
    _rec_name = "property_id"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    property_id = fields.Many2one(
        comodel_name="payroll.plan.property",
        string="Tiêu chí",
        required=True,
        readonly=True,
        states={"unlock": [("readonly", False)]},
        track_visibility="onchange",
    )
    company_id = fields.Many2one('res.company', related='property_id.company_id', string='Công ty',store=True)
    report_id = fields.Many2one(
        "payroll.report",
        string="Báo cáo tháng",
        required=True,
        ondelete="cascade",
        readonly=True,
        states={"unlock": [("readonly", False)]},
        track_visibility="onchange",
    )
    amount = fields.Float(
        "Thực hiện tháng trước",
        readonly=True,
        states={"unlock": [("readonly", False)]},
        track_visibility="onchange",
    )
    estimated_report_month = fields.Float(
        "Ước tính tháng báo cáo",
        readonly=True,
        states={"unlock": [("readonly", False)]},
        track_visibility="onchange",
    )
    cumulative_year = fields.Float(
        "Cộng dồn năm",
        compute='compute_cumulative_year'
    )
    month = fields.Selection(
        "Tháng",
        related="report_id.month",
        store=True,
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

    string_month = fields.Date('Tháng', compute='update_month', store=True)

    @api.one
    @api.depends('month')
    def update_month(self):
        day = "02"
        month = self.month
        year = self.report_id[0].plan_id[0].year
        string_date = str(year) + '-' + str(month) + '-' + str(day)
        date_time_obj = dt.datetime.strptime(string_date, '%Y-%m-%d')
        self.string_month = date_time_obj.date()

    def compute_cumulative_year(self):
        for em in self:
            em.cumulative_year = 0
            for line in em.report_id.plan_id.line_report_ids:
                if int(line.month) <= int(em.report_id.month):
                    for li in line.line_ids:
                        if li.property_id == em.property_id:
                            em.cumulative_year = em.cumulative_year + li.amount

    @api.model
    def create(self, values):
        # Add code here
        res = super(PayrollReportLine, self).create(values)
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
        return super(PayrollReportLine, self).unlink()
    
    def open_payroll_report(self):
        return {
            'name': _('Báo cáo tiền lương của đơn vị'),
            'res_id': self.id,
            'view_type': 'form',
            'res_model': 'payroll.report_line',
            'view_id': False,
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
        }

# Tao bao cao
class PayrollReport(models.Model):
    _name = "payroll.report"
    _rec_name = "name"
    _description = "Báo cáo tháng"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char("Tên", compute="compute_name")
    plan_id = fields.Many2one(
        "payroll.report.year.plan",
        string="Thuộc kế hoạch",
        required=True,
        ondelete="cascade",
    )
    month = fields.Selection(
        string="Tháng",
        selection=[
            ("01", "Tháng 1"),
            ("02", "Tháng 2"),
            ("03", "Tháng 3"),
            ("04", "Tháng 4"),
            ("05", "Tháng 5"),
            ("06", "Tháng 6"),
            ("07", "Tháng 7"),
            ("08", "Tháng 8"),
            ("09", "Tháng 9"),
            ("10", "Tháng 10"),
            ("11", "Tháng 11"),
            ("12", "Tháng 12"),
        ],
        default=(time.strftime("%m")),
        track_visibility="always",
    )
    line_ids = fields.One2many(
        comodel_name="payroll.report_line",
        inverse_name="report_id",
        string="Báo cáo tháng của các đơn vị",
    )


    _sql_constraints = [
        (
            "payroll_report_uniq",
            "unique (plan_id, month)",
            "Đã tồn tại báo cáo cho tháng này!",
        )
    ]

    @api.multi
    @api.returns("mail.message", lambda value: value.id)
    def message_post(self, **kwargs):
        return super(
            PayrollReport, self.with_context(mail_post_autofollow=True)
        ).message_post(**kwargs)

    def lock_data(self):
        list_report = self.env["payroll.report_line"].search(
            [("report_id", "=", self.id)]
        )
        for line in list_report:
            line.state = "lock"
        return True

    def unlock_data(self):
        list_report = self.env["payroll.report_line"].search(
            [("report_id", "=", self.id)]
        )
        for line in list_report:
            line.state = "unlock"
        return True

    @api.depends("month")
    def compute_name(self):
        for em in self:
            if em.plan_id:
                em.name = "Báo cáo nhanh lao động tiền lương " +  "tháng " + str(
                    em.month) + '-' + str(em.plan_id.year)

    def generate_report_line(self):
        if len(self.plan_id.list_property_ids) == 0:
            raise UserError('Bạn cần chọn danh sách tiêu chí trong kế hoạch năm để tạo dòng cáo cáo')
        list_pro = []
        for line in self.line_ids:
            if line.property_id not in list_pro:
                list_pro.append(line.property_id)

        for line in self.plan_id.list_property_ids:
            if line not in list_pro:
                self.env['payroll.report_line'].create({
                    'property_id': line.id,
                    'report_id': self.id,
                })


    @api.model
    def create(self, values):
        # Add code here
        res = super(PayrollReport, self).create(values)
        msg = _("Dòng %s được thêm vào báo cáo") % (res.name)
        res.plan_id.message_post(body=msg)
        return res

    @api.multi
    def unlink(self):
        for em in self:
            msg = _("Báo cáo tháng %s được <strong>xóa</strong> khỏi kế hoạch") % (
                em.month
            )
            em.plan_id.message_post(body=msg)
        return super(PayrollReport, self).unlink()

    @api.multi
    def create_report(self):
        reports = self.env["payroll.report.property"].search(
            [("report_id", "=", self.id)]
        )
        reports.unlink()

        amount_plan = dict()
        for line in self.plan_id.line_ids:
            if line.property_id not in amount_plan.keys():
                amount_plan[line.property_id] = 0
                amount_plan[line.property_id] = amount_plan[line.property_id] + line.expected_year_amount
            else:
                amount_plan[line.property_id] = amount_plan[line.property_id] + line.expected_year_amount

            property_1 = ""
            property_2 = ""
            property_3 = ""

            if len(line.property_id.property_ids) == 1:
                property_1 = line.property_id.property_ids[0].name
            elif len(line.property_id.property_ids) == 2:
                property_1 = line.property_id.property_ids[0].name
                property_2 = line.property_id.property_ids[1].name
            elif len(line.property_id.property_ids) >= 3:
                property_1 = line.property_id.property_ids[0].name
                property_2 = line.property_id.property_ids[1].name
                property_3 = line.property_id.property_ids[2].name


            self.env['payroll.report.property'].create({
                'property_1': property_1,
                'property_2': property_2,
                'property_3': property_3,
                'label_l1':"Báo cáo nhanh lao động tiền lương tháng "+ self.month+" năm "+str(self.plan_id.year),
                'label_l2': "1. Kế hoạch năm",
                'report_id': self.id,
                'amount': line.expected_year_amount,
            })


        for line in self.line_ids:
            property_1 = ""
            property_2 = ""
            property_3 = ""
            if len(line.property_id.property_ids) == 1:
                property_1 = line.property_id.property_ids[0].name
            elif len(line.property_id.property_ids) == 2:
                property_1 = line.property_id.property_ids[0].name
                property_2 = line.property_id.property_ids[1].name
            elif len(line.property_id.property_ids) >= 3:
                property_1 = line.property_id.property_ids[0].name
                property_2 = line.property_id.property_ids[1].name
                property_3 = line.property_id.property_ids[2].name


            self.env['payroll.report.property'].create({
                'property_1': property_1,
                'property_2': property_2,
                'property_3': property_3,
                'label_l1': "Báo cáo nhanh lao động tiền lương tháng "+ self.month+" năm "+str(self.plan_id.year),
                'label_l2': "2. Thực hiện tháng trước",
                'report_id': self.id,
                'amount': line.amount,
            })
            self.env['payroll.report.property'].create({
                'property_1': property_1,
                'property_2': property_2,
                'property_3': property_3,
                'label_l1': "Báo cáo nhanh lao động tiền lương tháng "+ self.month+" năm "+str(self.plan_id.year),
                'label_l2': "3. Ước tính tháng báo cáo",
                'report_id': self.id,
                'amount': line.estimated_report_month,
            })
            self.env['payroll.report.property'].create({
                'property_1': property_1,
                'property_2': property_2,
                'property_3': property_3,
                'label_l1': "Báo cáo nhanh lao động tiền lương tháng "+ self.month+" năm "+str(self.plan_id.year),
                'label_l2': "4. Cộng dồn năm",
                'report_id': self.id,
                'amount': line.cumulative_year,
            })
