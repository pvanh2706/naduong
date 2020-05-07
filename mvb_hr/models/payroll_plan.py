from odoo import api, fields, models, _
import time
from datetime import datetime
from odoo.exceptions import UserError

class PayrollPlanSubProperty(models.Model):
    _name = 'payroll.plan.sub.property'
    _rec_name = 'name'
    _description = 'New Description'
    _order = 'level, sequence'

    name = fields.Char('Tên')
    level = fields.Integer('Cấp độ')
    sequence = fields.Integer('Thứ tự')

class PayrollPlanProperty(models.Model):
    _name = 'payroll.plan.property'
    _rec_name = 'name'
    _description = 'New Description'

    name = fields.Char('Tên', compute='_compute_name', store=True)
    property_ids = fields.Many2many(comodel_name="payroll.plan.sub.property", string="Danh sách tiêu chí thành phần")
    unit = fields.Char('Đơn vị tính')
    company_id = fields.Many2one('res.company', string='Công ty', default=None)

    @api.depends('property_ids.name')
    def _compute_name(self):
        for em in self:
            em.name = ""
            for line in em.property_ids:
                em.name = str(em.name) + "[" + str(line.name) + "]"

    cop_id = fields.Integer('CoP ID', compute='compute_cop_id', store=True)

    @api.depends('company_id')
    def compute_cop_id(self):
        for em in self:
            if em.company_id:
                em.cop_id = em.company_id.id
            else:
                em.cop_id = 1000

    _sql_constraints = [
        ('payroll_property_uniq', 'unique (name, cop_id)',
         'Đã tồn tại tiêu chí này!')
    ]


class PayrollReportYearPlanLine(models.Model):
    _name = 'payroll.report.year.plan.line'
    _rec_name = 'name'
    _description = 'Dòng kế hoạch'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Tên', compute='compute_name')
    property_id = fields.Many2one(comodel_name="payroll.plan.property", string="Tiêu chí", required=True, track_visibility='onchange')
    year_plan_id = fields.Many2one('payroll.report.year.plan', string='Báo cáo năm', required=True, ondelete="cascade", track_visibility='onchange')
    company_id = fields.Many2one('res.company', related='property_id.company_id',string='Công ty')
    expected_year_amount = fields.Float('Giá trị năm', track_visibility='onchange')
    
    expected_month_1_amount = fields.Float('Giá trị Tháng 1', track_visibility='onchange')
    expected_month_2_amount = fields.Float('Giá trị Tháng 2', track_visibility='onchange')
    expected_month_3_amount = fields.Float('Giá trị Tháng 3', track_visibility='onchange')
    expected_month_4_amount = fields.Float('Giá trị Tháng 4', track_visibility='onchange')
    expected_month_5_amount = fields.Float('Giá trị Tháng 5', track_visibility='onchange')
    expected_month_6_amount = fields.Float('Giá trị Tháng 6', track_visibility='onchange')
    expected_month_7_amount = fields.Float('Giá trị Tháng 7', track_visibility='onchange')
    expected_month_8_amount = fields.Float('Giá trị Tháng 8', track_visibility='onchange')
    expected_month_9_amount = fields.Float('Giá trị Tháng 9', track_visibility='onchange')
    expected_month_10_amount = fields.Float('Giá trị Tháng 10', track_visibility='onchange')
    expected_month_11_amount = fields.Float('Giá trị Tháng 11', track_visibility='onchange')
    expected_month_12_amount = fields.Float('Giá trị Tháng 12', track_visibility='onchange')

    _sql_constraints = [
        ('payroll_plan_property_id_uniq', 'unique (property_id, year_plan_id)',
         'Một tiêu chí chỉ có thể có một kế hoạch năm của năm đó!')
    ]

    @api.depends('year_plan_id')
    def compute_name(self):
        for em in self:
            if em.property_id:
                em.name = "Kế hoạch lao động tiền lương " +str(em.year_plan_id.year) + " cho "+ em.property_id.name


    @api.model
    def create(self, values):
        # Add code here
        res = super(PayrollReportYearPlanLine, self).create(values)
        msg = _('Dòng %s được thêm vào kế hoạch') % (res.name)
        res.year_plan_id.message_post(body=msg)
        return res

    @api.multi
    def unlink(self):
        for em in self:
            msg = _('Dòng %s được <strong>xóa</strong> khỏi kế hoạch') % (em.name)
            em.year_plan_id.message_post(body=msg)
        return super(PayrollReportYearPlanLine, self).unlink()


class PayrollReportYearPlan(models.Model):
    _name = 'payroll.report.year.plan'
    _rec_name = 'name'
    _description = 'Kế hoạch năm'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Tên', compute='compute_name')
    year = fields.Selection([(num, str(num)) for num in range(1999, (datetime.now().year) + 50)], 'Năm',
                            default=int((time.strftime('%Y'))), track_visibility='always')
    line_ids = fields.One2many(comodel_name="payroll.report.year.plan.line", inverse_name="year_plan_id", string="Kế hoạch theo tiêu chí" )
    line_report_ids = fields.One2many(comodel_name="payroll.report", inverse_name="plan_id",
                               string="Báo cáo tháng")
    list_property_ids = fields.Many2many('payroll.plan.property', string='Danh sách tiêu chí')

    @api.depends('year')
    def compute_name(self):
        for em in self:
            em.name = "Kế hoạch lao động tiền lương " + str(em.year)

    @api.multi
    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        return super(PayrollReportYearPlan, self.with_context(mail_post_autofollow=True)).message_post(**kwargs)

    def generate_plan_line(self):
        if len(self.list_property_ids) == 0:
            raise UserError('Bạn cần chọn danh sách tiêu chí để tạo kế hoạch')
        list_pro = []
        for line in self.line_ids:
            if line.property_id not in list_pro:
                list_pro.append(line.property_id)

        for line in self.list_property_ids:
            if line not in list_pro:
                self.env['payroll.report.year.plan.line'].create({
                    'property_id': line.id,
                    'year_plan_id': self.id,
                })