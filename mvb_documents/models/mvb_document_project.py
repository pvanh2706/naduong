
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _
import re

class DocumentProjectPhase(models.Model):
    _name = 'mvb.document.project.phase'
    _description = 'Tài liệu giai đoạn gói thầu'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char('Tên giai đoạn')
    phase_code = fields.Char('Mã giai đoạn')
    phase_content = fields.Text('Nội dung giai đoạn')
    project_phase_id = fields.Many2one(comodel_name="mvb.document.project", string="Tên dự án")


class DocumentBiddingPackage(models.Model):
    _name = 'mvb.document.bidding.package'
    _description = 'Tài liệu gói thầu'

    bidding_code = fields.Char('Mã gói thầu')
    name = fields.Char('Tên gói thầu')

    type_bidding = fields.Selection([('dt_rongrai', 'Đấu thầu rộng rãi'), ('dt_hanche', 'Đấu thầu hạn chế'),
                                     ('chidinhdauthau', 'Chỉ định thầu'),
                                     ('chaohangcanhtranh', 'Chào hàng cạnh tranh'),
                                     ('muasamtructuyen', 'Mua sắm trực tiếp'),
                                     ('tuthuchien', 'Tự thực hiện'),
                                     ('dt_dacbiet', 'Lựa chọn nhà thầu trong trường hợp đặc biệt'),
                                     ('dt_congdong', 'Tham gia thực hiện của cộng đồng')
                                     ], default='dt_rongrai', string="Hình thức lựa chọn nhà thầu")
    method_bidding = fields.Selection([
        ('method_1', '1 giai đoạn 1 túi hồ sơ'),
        ('method_2', '1 giai đoạn 2 túi hồ sơ'),
        ('method_3', '2 giai đoạn 1 túi hồ sơ'),
        ('method_4', '2 giai đoạn 2 túi hồ sơ'),
    ], string='Phương thức lựa chọn nhà thầu', default='method_1')

    field_bidding = fields.Selection([
        ('hanghoa', 'Mua sắm hàng hóa'),
        ('xaylap', 'Xây lắp'),
        ('tuvan', 'Tư vấn'),
        ('phituvan', 'Phi Tư vấn'),
        ('honhop', 'Hỗn hợp'),
    ], string="Lĩnh vực đấu thầu", default='hanghoa')

    project_id = fields.Many2one(comodel_name="mvb.document.project", string="Tên dự án")
    # project_name = fields.Char("Tên dự án", related='project_id.name')

    cost_bidding = fields.Float(string="Giá gói thầu", digits=(3, 2))
    capital_source = fields.Char("Nguồn vốn")
    time_to_start = fields.Char("Thời gian bắt đầu tổ chức lựa chọn nhà thầu")
    type_contract = fields.Char("Loại hợp đồng")
    duration_of_contract = fields.Char("Thời gian thực hiện hợp đồng")

    @api.multi
    @api.constrains('bidding_code','name')
    def validate_bidding(self):
        if self.bidding_code == False:
            raise ValidationError(_("Bạn phải nhập mã gói thầu"))
        if self.name == False:
            raise ValidationError(_("Bạn cần nhập tên gói thầu"))

    # @api.multi
    # def name_get(self):
    #     def _name_get(d):
    #         name = d.get('name', '')
    #         project_name = d.get('project_name', False) or ''
    #         if project_name:
    #             name = '[%s] %s' % (project_name, name)
    #         return (d['id'], name)

    #     self.check_access_rights("read")
    #     self.check_access_rule("read")

    #     result = []
    #     for mnv in self.sudo():
    #         mydict = {
    #             'id'  : mnv.id,
    #             'name': mnv.name,
    #             'project_name': mnv.project_id.name,
    #         }
    #         result.append(_name_get(mydict))
    #     return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike',
                     limit=100, name_get_uid=None):
        print("===", args)
        args = [] if args is None else args.copy()
        if not (name == '' and operator == 'ilike'):
            args += ['|',
                     ('name', operator, name),
                     ('project_id.name', operator, name)
                     ]
            bidding_ids = self.search(args).ids
            return self.browse(bidding_ids).name_get()
        return super(DocumentBiddingPackage, self)._name_search(
            name=name, args=args, operator=operator,
            limit=limit, name_get_uid=name_get_uid)
    # @api.model
    # def name_search(self, name='', args=None, operator='ilike', limit=100):
    #     if not args:
    #         args = []
    #     if name:
    #         positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
    #         employees = self.env['hr.employee']
    #         if operator in positive_operators:
    #             employees = self.search(
    #                 [('employee_code', '=', name)] + args,
    #                 limit=limit)
    #         if not employees and operator not in expression.NEGATIVE_TERM_OPERATORS:
    #             # Do not merge the 2 next lines into one single search, SQL search performance would be abysmal
    #             # on a database with thousands of matching employees, due to the huge merge+unique needed for the
    #             # OR operator (and given the fact that the 'name' lookup results come from the ir.translation table
    #             # Performing a quick memory merge of ids in Python will give much better performance
    #             employees = self.search(
    #                 args + [
    #                     ('employee_code', operator, name)
    #                 ],
    #                 limit=limit)
    #             if not limit or len(employees) < limit:
    #                 # we may underrun the limit because of dupes in the results, that's fine
    #                 limit2 = (limit - len(employees)) if limit else False
    #                 employees += self.search(
    #                     args + [('name', operator, name),
    #                             ('id', 'not in', employees.ids)],
    #                     limit=limit2)
    #         elif not employees and operator in expression.NEGATIVE_TERM_OPERATORS:
    #             domain = expression.OR([
    #                 [
    #                     '&', ('employee_code', operator, name),
    #                     ('name', operator, name)
    #                 ],
    #                 [
    #                     '&', ('employee_code', operator, name),
    #                     ('name', operator, name)
    #                 ],
    #             ])
    #             domain = expression.AND([args, domain])
    #             employees = self.search(domain, limit=limit)
    #         if not employees and operator in positive_operators:
    #             ptrn = re.compile('(\[(.*?)\])')
    #             res = ptrn.search(name)
    #             if res:
    #                 employees = self.search(
    #                     [
    #                         ('employee_code', '=', res.group(2))
    #                     ] + args,
    #                     limit=limit)
    #     else:
    #         employees = self.search(args, limit=limit)
    #     return employees.name_get()



class DocumentProject(models.Model):
    _name = 'mvb.document.project'
    _description = 'Tài liệu dự án'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    project_code = fields.Char('Mã dự án/phương án')
    name = fields.Char('Tên dự án/phương án')
    number_of_project_approval = fields.Char("Số quyết định phê duyệt")
    date_project_approval = fields.Date("Ngày phê duyệt")
    investor = fields.Char("Chủ đầu tư")

    investment_location = fields.Char("Địa điểm đầu tư")
    type_investment = fields.Char("Hình thức đầu tư")
    total_investment = fields.Float('Tổng mức đầu tư', digits=(16,2))
    investment_funds = fields.Char("Nguồn vốn đầu tư")
    is_have_bidding = fields.Boolean('Không có gói thầu', default=False)

    @api.multi
    def write(self, values):
        # Add code here
        if values.get('name'):
            bidding = self.env['mvb.document.biddingstate'].search([('project_name','=',self.name)])
            if bidding:
                for rec in bidding:
                    update_name_project = {
                        'project_name': values.get('name'),
                    }
                    rec.write(update_name_project)
        if values.get('is_have_bidding') == True:
            bidding = self.env['mvb.document.bidding.package'].search([])
            for rec in bidding:
                if rec.project_id.id == self.id:
                    raise ValidationError(_('Dự án này đã có gói thầu. Bạn không thể đánh dấu là không có gói thầu nào!'))
        return super(DocumentProject, self).write(values)