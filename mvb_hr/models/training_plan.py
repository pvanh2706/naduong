from odoo import api, fields, models, _
import time
from datetime import datetime
from odoo.exceptions import UserError

class TrainPlanSubProperty(models.Model):
    _name = 'train.plan.sub.property'
    _rec_name = 'name'
    _description = 'New Description'
    _order = 'level, sequence'
    
    sequence = fields.Integer("Thứ tự")
    name = fields.Char('Tên')
    level = fields.Integer('Cấp độ')

class TrainPlanProperty(models.Model):
    _name = 'train.plan.property'
    _rec_name = 'name'
    _order = 'sequence'
    _description = 'New Description'

    sequence = fields.Integer("Thứ tự")
    name = fields.Char('Tên', compute='_compute_name', store=True)
    property_ids = fields.Many2many(comodel_name="train.plan.sub.property", string="Nội dung đào tạo, bồi dưỡng")
    company_id = fields.Many2one(
        "res.company", string="Công ty"
    )
    short_name = fields.Char('Tiêu chí báo cáo', compute="_compute_name")

    @api.depends("property_ids.name")
    def _compute_name(self):
        for em in self:
            em.name = ""
            em.short_name = ""
            for line in em.property_ids:
                em.name = str(em.name) + "[" + str(line.name) + "]"
                if line.id != em.property_ids[0].id:
                    em.short_name = str(em.short_name) + "[" + str(line.name) + "]"


class TrainReportYearPlanLine(models.Model):
    _name = 'train.report.year.plan.line'
    _rec_name = 'name'

    name = fields.Char('Tên', compute='compute_name')
    property_id = fields.Many2one(comodel_name="train.plan.property", string="Tiêu chí", required=True)
    year_plan_id = fields.Many2one('train.report.year.plan', string='Báo cáo năm', required=True, ondelete="cascade")
    year_input = fields.Selection('Năm', related='year_plan_id.year', store=True)
    year = fields.Char('Năm', compute='compute_name')

    attendees_expected_amount = fields.Integer('Số người dự học')
    company_expected_amount = fields.Float('Công ty')
    group_expected_amount = fields.Float('Tập đoàn')
    other_expected_amount = fields.Float('Khác')
    total_expected_amount = fields.Float('Tổng số', compute='compute_total_expected')
    short_name = fields.Char('Tiêu chí báo cáo', compute='compute_short_name')
    company_id = fields.Many2one(
        "res.company",
        "Công ty",
        related="property_id.company_id", store = True
    )

    @api.depends("property_id")
    def compute_short_name(self):
        for em in self:
            em.short_name = em.property_id.short_name

    _sql_constraints = [
        ('train_plan_property_id_uniq', 'unique (property_id, year_input)',
         'Một tiêu chí chỉ có thể có một kế hoạch năm của năm đó!')
    ]

    @api.depends('company_expected_amount', 'group_expected_amount','other_expected_amount')
    def compute_total_expected(self):
        for em in self:
            em.total_expected_amount = em.company_expected_amount + em.group_expected_amount + em.other_expected_amount


    @api.depends('year_input')
    def compute_name(self):
        for em in self:
            if em.property_id:
                em.name = "Kế hoạch thực hiện công tác đào tạo, bồi dưỡng năm " +str(em.year_input)
                em.year = str(em.year_input)

    def open_training_plan(self):
        return {
            'name': _('Kế hoạch năm kế tiếp'),
            'res_id': self.id,
            'view_type': 'form',
            'res_model': 'train.report.year.plan.line',
            'view_id': False,
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
        }

    @api.model
    def create(self, values):
        # Add code here
        res = super(TrainReportYearPlanLine, self).create(values)
        msg = _('Dòng %s được thêm vào kế hoạch') % (res.name)
        res.year_plan_id.message_post(body=msg)
        return res


class TrainReportYearPlan(models.Model):
    _name = 'train.report.year.plan'
    _rec_name = 'name'
    _description = 'Kế hoạch năm'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Tên', compute='compute_name')
    year = fields.Selection([(num, str(num)) for num in range(1999, (datetime.now().year) + 50)], 'Năm',
                            default=int((time.strftime('%Y'))), track_visibility='always')
    line_ids = fields.One2many(comodel_name="train.report.year.plan.line", inverse_name="year_plan_id", string="Kế hoạch theo tiêu chí" )
    line_report_ids = fields.One2many(comodel_name="train.report", inverse_name="plan_id",
                               string="Báo cáo tháng")
    list_property_ids = fields.Many2many('train.plan.property', string='Danh sách tiêu chí')

    @api.depends('year')
    def compute_name(self):
        for em in self:
            em.name = "Kế hoạch thực hiện công tác đào tạo, bồi dưỡng năm " + str(em.year)

    @api.multi
    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        return super(TrainReportYearPlan, self.with_context(mail_post_autofollow=True)).message_post(**kwargs)
    
    def generate_plan_line(self):
        if len(self.list_property_ids) == 0:
            raise UserError('Bạn cần chọn danh sách tiêu chí để tạo kế hoạch')
        list_pro = []
        for line in self.line_ids:
            if line.property_id not in list_pro:
                list_pro.append(line.property_id)

        for line in self.list_property_ids:
            if line not in list_pro:
                self.env['train.report.year.plan.line'].create({
                    'property_id': line.id,
                    'year_plan_id': self.id,
                })


