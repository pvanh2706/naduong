from odoo import api, fields, models
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.osv import expression
import re


class HrMVBEmployee(models.Model):
    _inherit = 'hr.employee'
    _description = 'Sơ yêu lý lịch'
    _order = 'level_id'

    user_id = fields.Many2one('res.users', 'User', domain="[]", readonly=False)
    login_id = fields.Char(related='user_id.login', string="Tài khoản")
    level_id = fields.Integer(string="Cấp độ hiển thị ưu tiên", help="Thứ tự hiển thị", default="100")
    position_history_ids = fields.One2many(comodel_name="hr.position.history",
                                           inverse_name="employee_id",
                                           string="Tóm tắt quá trình công tác")
    employee_code = fields.Char(string="Mã nhân viên")
    age = fields.Integer(string="Age", compute='_compute_age', store=True)
    birth_place = fields.Many2one('current.address', 'Nơi sinh')
    current_address = fields.Many2one('current.address', 'Nơi ở hiện tại')
    hometown_state_id = fields.Many2one('current.address', 'Quê quán')

    total_employees = fields.Char('Tổng', default='Tổng', required=True)

    _sql_constraints = [
        ('employee_code_uniq', 'unique (employee_code)',
         'Mã nhân viên này đã tồn tại!')
    ]

    @api.depends('birthday')
    def _compute_age(self):
        """Updates age field when birth_date is changed"""
        for em in self:
            if em.birthday:
                d1 = em.birthday
                d2 = date.today()
                em.age = relativedelta(d2, d1).years

    @api.multi
    def write(self, vals):
        lst_job = {}
        if vals.get('job_id'):
            self.user_id.write({'mvb_job_name': self.env['hr.job'].browse(vals.get('job_id')).name, 'mvb_department_name': self.env['hr.job'].browse(vals.get('job_id')).department_id.name})
            for employee in self:
                lst_job.update({employee: employee.job_id})

        res = super(HrMVBEmployee, self).write(vals)
        if vals.get('user_id'):
            update_user = self.env['res.users'].browse(vals.get('user_id'))
            if len(update_user) > 0:
                update_user.mvb_department_name = self.department_id.name
                update_user.mvb_job_name = self.job_id.name
                update_user.is_choose = True
                if self.user_id.is_choose == True:
                    self.user_id.is_choose = False

        # if lst_job:
        #     hr_position_history = self.env['hr.position.history']
        #     for employee in lst_job.keys():
        #         today = fields.Date.context_today(self)
        #         hr_position_history.create({
        #             'employee_id':
        #             employee.id,
        #             'date':
        #             today,
        #             'old_position_id':
        #             lst_job[employee] and lst_job[employee].id or False,
        #             'new_position_id':
        #             employee.job_id and employee.job_id.id or False,
        #         })
        return res

    job_import = fields.Char('Vị trí công việc đầu vào', default="0")

    @api.model
    def create(self, values):
        if values.get('job_import') != "0":
            input = values.get('job_import')
            a = input.split("[")
            job = a[2].split("] ")[1]
            department = a[2].split("] ")[0]
            company = a[1].split("] ")[0]
            # print (company)
            # print (department)
            job_ids = self.env['hr.job'].search([('name', '=', job)])
            # print(job_id)
            job_id = 0
            for line in job_ids:
                if line.department_id.name == department and line.company_id.code == company:
                    job_id = line.id
                    break
            print(job_id)
            values.update({'job_id': job_id})
        res = super(HrMVBEmployee, self).create(values)
        if res.user_id:
            res.user_id.mvb_department_name = res.department_id.name
            res.user_id.mvb_job_name = res.job_id.name
            res.user_id.is_choose = True
        # if values.get('job_id'):
        #     today = fields.Date.context_today(self)
        #     self.env['hr.position.history'].create({
        #             'employee_id': res.id,
        #             'date': today,
        #             'position_id': values.get('job_id') or False,
        #         })

        return res

    other_name = fields.Char(string="Tên gọi khác")
    ethnic = fields.Many2one("ethnic.group", "Dân tộc")
    religion = fields.Char(string="Tôn giáo")
    family_composition_comes_from = fields.Char(string="Thành phần xuất thân gia đình")
    job_before_recruitment = fields.Char(
        string="Nghề nghiệp bản thân trước khi được tuyển dụng")
    day_recruitment = fields.Date(string="Ngày được tuyển dụng")
    first_work_day = fields.Date(string="Ngày vào cơ quan hiện đang công tác")
    day_join_revolution = fields.Date(string="Ngày tham gia cách mạng")
    day_join_DCSVN = fields.Date(string="Ngày vào Đảng cộng sản Việt Nam")
    day_officer = fields.Date(string="Ngày chính thức")
    day_join_social_and_political_organizations = fields.One2many(
        string="Ngày tham gia các tổ chức chính trị, xã hội",
        help="Đoàn TNCS Hồ Chí Minh, Công đoàn, Hội.....",
        comodel_name='hr.political.organizations',
        inverse_name='employee_id')
    date_of_enlistment = fields.Date(string="Ngày nhập ngũ")
    demobilization_day = fields.Date(string="Ngày xuất ngũ")
    rank = fields.Char(string="Quân hàm, chức vụ cao nhất (năm)")

    general_education = fields.Char(string="Giáo dục phổ thông")

    highest_position_education = fields.Selection(
        string="Học hàm - học vị cao nhất",
        selection=[('ths', 'Thạc sỹ'), ('ts', 'Tiến sỹ'),
                   ('dhkth', 'Đại học-Kỹ thuật'), ('dhkt', 'Đại học-Kinh tế'),
                   ('dhk', 'Đại học-Khác'), ('cdkth', 'Cao đẳng-Kỹ thuật'),
                   ('cdkt', 'Cao đẳng-Kinh tế'), ('cdk', 'Cao đẳng-Khác'),
                   ('tckth', 'Trung cấp-Kỹ thuật'),
                   ('tckt', 'Trung cấp-Kinh tế'), ('tck', 'Trung cấp-Khác')],
        required=False,
    )
    political_theory = fields.Selection(
        string="Lý luận chính trị",
        selection=[
            ('llsc', 'Sơ cấp'),
            ('lltc', 'Trung cấp'),
            ('llcn', 'Cử nhân'),
            ('llnc', 'Cao cấp'),
        ],
        required=False,
    )
    foreign_language = fields.Char(string="Ngoại ngữ")
    major_qualification = fields.Char(string="Trình độ chuyên môn chính")
    main_work_is_doing = fields.Char(string="Công tác chính đang làm")
    current_salary = fields.Char(string="Lương hiện hưởng")
    study_process_id = fields.One2many(string="Quá trình học tập",
                                       comodel_name="hr.study.process",
                                       inverse_name="employee_id")
    major = fields.Char(string="Lớp đào tạo", required=False, related="study_process_id.major")
    ngach_cong_chuc_id = fields.Many2one(string="Lương hiện hưởng",
                                         comodel_name="hr.ngach.cong.chuc")
    label = fields.One2many(
        string="Danh hiệu được phong(năm nào)",
        help=
        "Anh hùng lao động, Anh hùng lực lượng vũ trang; nhà giáo, thày thuốc, nghệ sỹ nhân dân, ưu tú",
        comodel_name='hr.label',
        inverse_name='employee_id')
    forte = fields.Text(string="Sở trường công tác")
    work_longest = fields.Char(string="Công việc đã làm lâu nhất")
    bonus = fields.One2many(string="Khen thưởng",
                            help="Huân chương, huy chương, năm nào",
                            comodel_name='hr.bonus',
                            inverse_name='employee_id')
    medal = fields.Char(string="Khen thưởng", required=False, related="bonus.medal")
    discipline = fields.One2many(
        string="Kỷ luật",
        help=
        "Hành chính, đảng, đoàn thể, cấp quyết định, năm nào, lý do, hình thức",
        comodel_name='hr.discipline',
        inverse_name='employee_id')
    health_status = fields.Text(
        string="Tình trạng sức khỏe",
        help="Tốt, bình thường, yếu hoặc có bệnh mãn tính gì")
    height = fields.Float(string="Chiều cao (cm)")
    weight = fields.Float(string="Cân nặng (kg)")
    blood_group = fields.Char(string="Nhóm máu")
    release_date_CMND = fields.Date(string="Ngày cấp CMND")
    veteran_type = fields.Char(string="Thương binh loại")
    is_family_of_martyrs = fields.Boolean(string="Gia đình liệt sỹ")
    family_relationship_of_me_id = fields.One2many(
        string="Quan hệ gia đình tôi",
        comodel_name='hr.family.relationship',
        inverse_name='employee_id1')
    family_relationship_of_partner_id = fields.One2many(
        string="Quan hệ gia đình vợ (chồng) tôi",
        comodel_name='hr.family.relationship',
        inverse_name='employee_id2')
    salary_process_id = fields.One2many(string='Quá trình lương bản thân',
                                        comodel_name='hr.salary.process',
                                        inverse_name='employee_id')

    total_salary_family = fields.Float(string="Lương gia đình")
    salary_husband = fields.Float(string="Lương Chồng")
    salary_wife = fields.Float(string="Lương Vợ")
    other_money = fields.Float(
        string="Các nguồn khác",
        help="Lãi tiết kiệm, cổ tức, tư vấn quản lý và tư vấn kinh doanh")
    house_area = fields.Float(
        string="Được cấp, được thuê, loại nhà, tổng diện tích dử dụng (m2)")
    house_type = fields.Char(string="Nhà tự mua, tự xây, loại nhà")

    land_granted = fields.Float(string="Đất được cấp (m2)")
    land_purchased = fields.Float(string="Đất tự mua (m2)")

    land_production_business = fields.Float(
        string="Đất sản xuất, kinh doanh (m2)",
        help="Tổng diện tích đất đươc cấp, tự mua, tự khai phá...")

    is_to_jail = fields.Boolean(string="Đã từng đi tù, bị bắt")
    info_to_jail = fields.Text(
        string="Lý do bị bắt, đi tù",
        help="Từ ngày, tháng năm nào, đến ngày tháng năm nào")

    is_work_old_regime = fields.Boolean(string="Từng làm việc ở chế độ cũ")
    info_old_regime = fields.Text(
        string="Thông tin về chế độ cũ đã làm",
        help=
        "cơ quan, đơn vị nào, địa điểm, chức danh, chức vụ, thời gian làm việc"
    )

    is_join_foreign_organization = fields.Boolean(
        string="Tham gia hoặc quan hệ với tổ chức, chính trị kinh tế nước ngoài"
    )
    info_foreigin_organization = fields.Text(
        string="Thông tin tổ chức kinh kế nước ngoài",
        help="làm gì, tổ chức nào, đặt trụ sở ở đâu")

    is_relatives_foreiger = fields.Boolean(string="Có thân nhân nước ngoài")
    info_relatives_foreiger = fields.Text(
        string="Thông tin thân nhân nước ngoài",
        help="Bố, mẹ , vợ, chồng, con ,anh chị em ruột, làm gì, địa chỉ")
    identity_papers_ids = fields.One2many(comodel_name="hr.document",
                                          inverse_name="employee_id",
                                          string="ID papers")

    certificate_ids = fields.One2many(comodel_name="hr.document",
                                      inverse_name="employee_id2",
                                      string="Certificate")

    document_status = fields.Selection([
        ('incomplete', 'Chưa đủ hồ sơ'),
        ('completed', 'Đủ hồ sơ'),
    ],
        'Trạng thái',
        default="incomplete",
        compute="_check_employee_document")
    company_id = fields.Many2one(string="Công ty",
                                 related="job_id.company_id",
                                 store=True,
                                 readonly=True)
    department_id = fields.Many2one(related='job_id.department_id',
                                    string='Phòng ban',
                                    readonly=True,
                                    store=True)
    concurrent_positions = fields.Char(string="Chức vụ kiêm nhiệm")
    email = fields.Char(string="Email")
    personal_tax_code = fields.Char(string="Mã số thuế cá nhân")
    bhxh_code = fields.Char(string="Số sổ bảo hiểm xã hội")
    passport = fields.Char(string="Số hộ chiếu")

    attach_passport_peopleId = fields.Binary(string="Hộ chiếu/CMTND")
    attach_passport_peopleId_name = fields.Char("Tên file")

    attach_degree = fields.Binary(string="Bằng cấp")
    attach_degree_name = fields.Char("Tên file")

    attach_cv = fields.Binary(string="Sơ yếu lý lịch")
    attach_cv_name = fields.Char("Tên file")

    attach_health_certification = fields.Binary(string="Giấy khám sức khỏe")
    attach_health_certification_name = fields.Char("Tên file")

    attach_birth_certificate = fields.Binary(string="Giấy khai sinh")
    attach_birth_certificate_name = fields.Char("Tên file")

    attach_registration_book = fields.Binary(string="Sổ hộ khẩu")
    attach_registration_book_name = fields.Char("Tên file")

    orther_infomation = fields.One2many(comodel_name='hr.document',
                                        inverse_name='employee_id3',
                                        string="Tài liệu hồ sơ khác")

    other_files = fields.Many2many(comodel_name="ir.attachment", string="Thêm Tài liệu hồ sơ khác", )

    # def get_employee_code(self, id, company_id):

    #     datas = self.env['hr.employee'].search([('company_id', '=', company_id.id)])
    #     index = len(datas)
    #     code_company = ''
    #     if company_id.code:
    #         code_company = company_id.code
    #     res = code_company + str(id).zfill(5)
    #     return res

    @api.multi
    def name_get(self):
        def _name_get(d):
            name = d.get('name', '')
            employee_code = d.get('employee_code', False) or ''
            if employee_code:
                name = '[%s] %s' % (employee_code, name)
            return (d['id'], name)

        self.check_access_rights("read")
        self.check_access_rule("read")

        result = []
        for mnv in self.sudo():
            mydict = {
                'id': mnv.id,
                'name': mnv.name,
                'employee_code': mnv.employee_code,
            }
            result.append(_name_get(mydict))
        return result

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if not args:
            args = []
        if name:
            positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
            employees = self.env['hr.employee']
            if operator in positive_operators:
                employees = self.search(
                    [('employee_code', '=', name)] + args,
                    limit=limit)
            if not employees and operator not in expression.NEGATIVE_TERM_OPERATORS:
                # Do not merge the 2 next lines into one single search, SQL search performance would be abysmal
                # on a database with thousands of matching employees, due to the huge merge+unique needed for the
                # OR operator (and given the fact that the 'name' lookup results come from the ir.translation table
                # Performing a quick memory merge of ids in Python will give much better performance
                employees = self.search(
                    args + [
                        ('employee_code', operator, name)
                    ],
                    limit=limit)
                if not limit or len(employees) < limit:
                    # we may underrun the limit because of dupes in the results, that's fine
                    limit2 = (limit - len(employees)) if limit else False
                    employees += self.search(
                        args + [('name', operator, name),
                                ('id', 'not in', employees.ids)],
                        limit=limit2)
            elif not employees and operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = expression.OR([
                    [
                        '&', ('employee_code', operator, name),
                        ('name', operator, name)
                    ],
                    [
                        '&', ('employee_code', operator, name),
                        ('name', operator, name)
                    ],
                ])
                domain = expression.AND([args, domain])
                employees = self.search(domain, limit=limit)
            if not employees and operator in positive_operators:
                ptrn = re.compile('(\[(.*?)\])')
                res = ptrn.search(name)
                if res:
                    employees = self.search(
                        [
                            ('employee_code', '=', res.group(2))
                        ] + args,
                        limit=limit)
        else:
            employees = self.search(args, limit=limit)
        return employees.name_get()

    # @api.depends('company_id.code')
    # def _compute_code(self):
    #     for em in self:
    #         if str(em.id).isdigit():
    #             em.update({
    #                 'employee_code': em.get_employee_code(em.id, em.job_id.company_id),
    #             })

    def _check_employee_document(self):
        for em in self:
            if em.attach_degree != None and em.attach_cv != None:
                em.document_status = 'completed'
            else:
                em.document_status = 'incomplete'

    def create_employee_report(self):
        employee_ids = self.env['hr.employee'].search([])
        report_lines = self.env['hr.employee.report'].search([])
        report_lines.unlink()
        for em in employee_ids:
            if em.gender == 'female':
                self.env['hr.employee.report'].create({
                    'employee_id':
                        em.id,
                    'name':
                        '1',
                    'job_position_group':
                        em.job_id.job_position_group,
                    'label':
                        'b. Phụ nữ',
                })
        for em in employee_ids:
            if em.ethnic != "Kinh":
                self.env['hr.employee.report'].create({
                    'employee_id':
                        em.id,
                    'name':
                        '2',
                    'job_position_group':
                        em.job_id.job_position_group,
                    'label':
                        'c. Dân tộc thiểu số',
                })
        for em in employee_ids:
            if em.day_join_DCSVN != False:
                self.env['hr.employee.report'].create({
                    'employee_id':
                        em.id,
                    'name':
                        '3',
                    'job_position_group':
                        em.job_id.job_position_group,
                    'label':
                        'a. Đảng viên',
                })

        for em in employee_ids:
            if em.demobilization_day != False:
                self.env['hr.employee.report'].create({
                    'employee_id':
                        em.id,
                    'name':
                        '4',
                    'job_position_group':
                        em.job_id.job_position_group,
                    'label':
                        'd. Bộ đội phục viên',
                })
        for em in employee_ids:
            if em.age < 31:
                self.env['hr.employee.report'].create({
                    'employee_id':
                        em.id,
                    'name':
                        '5',
                    'job_position_group':
                        em.job_id.job_position_group,
                    'label':
                        'e. Ít hơn 31 tuổi',
                })
            elif em.age > 30 and em.age < 46:
                self.env['hr.employee.report'].create({
                    'employee_id':
                        em.id,
                    'name':
                        '6',
                    'job_position_group':
                        em.job_id.job_position_group,
                    'label':
                        'f. Từ 31 đến 45 tuổi',
                })
            elif em.age > 45 and em.age < 56:
                self.env['hr.employee.report'].create({
                    'employee_id':
                        em.id,
                    'name':
                        '7',
                    'job_position_group':
                        em.job_id.job_position_group,
                    'label':
                        'g. Từ 46 đến 55 tuổi',
                })
            elif em.age > 55:
                self.env['hr.employee.report'].create({
                    'employee_id':
                        em.id,
                    'name':
                        '8',
                    'job_position_group':
                        em.job_id.job_position_group,
                    'label':
                        'h. Nhiều hơn 55 tuổi',
                })
        for em in employee_ids:
            if em.highest_position_education == 'ths':
                self.env['hr.employee.report'].create({
                    'employee_id':
                        em.id,
                    'name':
                        '9',
                    'job_position_group':
                        em.job_id.job_position_group,
                    'label':
                        'i. Thạc sỹ',
                })
            elif em.highest_position_education == 'ts':
                self.env['hr.employee.report'].create({
                    'employee_id':
                        em.id,
                    'name':
                        '10',
                    'job_position_group':
                        em.job_id.job_position_group,
                    'label':
                        'k. Tiến sỹ',
                })
            elif em.highest_position_education == 'dhkth':
                self.env['hr.employee.report'].create({
                    'employee_id':
                        em.id,
                    'name':
                        '11',
                    'job_position_group':
                        em.job_id.job_position_group,
                    'label':
                        'l. Đại học kỹ thuật',
                })
            elif em.highest_position_education == 'dhkt':
                self.env['hr.employee.report'].create({
                    'employee_id':
                        em.id,
                    'name':
                        '12',
                    'job_position_group':
                        em.job_id.job_position_group,
                    'label':
                        'm. Đại học kinh tế',
                })
            elif em.highest_position_education == 'dhk':
                self.env['hr.employee.report'].create({
                    'employee_id':
                        em.id,
                    'name':
                        '13',
                    'job_position_group':
                        em.job_id.job_position_group,
                    'label':
                        'n. Đại học khác',
                })
            elif em.highest_position_education == 'cdkth':
                self.env['hr.employee.report'].create({
                    'employee_id':
                        em.id,
                    'name':
                        '14',
                    'job_position_group':
                        em.job_id.job_position_group,
                    'label':
                        'o. Cao đẳng kỹ thuật',
                })
            elif em.highest_position_education == 'cdkt':
                self.env['hr.employee.report'].create({
                    'employee_id':
                        em.id,
                    'name':
                        '15',
                    'job_position_group':
                        em.job_id.job_position_group,
                    'label':
                        'p. Cao đẳng kinh tế',
                })
            elif em.highest_position_education == 'cdk':
                self.env['hr.employee.report'].create({
                    'employee_id':
                        em.id,
                    'name':
                        '16',
                    'job_position_group':
                        em.job_id.job_position_group,
                    'label':
                        'q. Cao đẳng khác',
                })
            elif em.highest_position_education == 'tckth':
                self.env['hr.employee.report'].create({
                    'employee_id':
                        em.id,
                    'name':
                        '17',
                    'job_position_group':
                        em.job_id.job_position_group,
                    'label':
                        'r. Trung cấp kỹ thuật',
                })
            elif em.highest_position_education == 'tckt':
                self.env['hr.employee.report'].create({
                    'employee_id':
                        em.id,
                    'name':
                        '18',
                    'job_position_group':
                        em.job_id.job_position_group,
                    'label':
                        's. Trung cấp kinh tế',
                })
            elif em.highest_position_education == 'tck':
                self.env['hr.employee.report'].create({
                    'employee_id':
                        em.id,
                    'name':
                        '19',
                    'job_position_group':
                        em.job_id.job_position_group,
                    'label':
                        't. Trung cấp khác',
                })
            elif em.highest_position_education == False:
                self.env['hr.employee.report'].create({
                    'employee_id':
                        em.id,
                    'name':
                        '20',
                    'job_position_group':
                        em.job_id.job_position_group,
                    'label':
                        'u. Công nhân',
                })
        for em in employee_ids:
            if em.political_theory == 'llcb':
                self.env['hr.employee.report'].create({
                    'employee_id':
                        em.id,
                    'name':
                        '21',
                    'job_position_group':
                        em.job_id.job_position_group,
                    'label':
                        'v. Lý luận chính trị cơ bản ',
                })
            elif em.political_theory == 'llnc':
                self.env['hr.employee.report'].create({
                    'employee_id':
                        em.id,
                    'name':
                        '22',
                    'job_position_group':
                        em.job_id.job_position_group,
                    'label':
                        'w. Lý luận chính nâng cao ',
                })

        report_ids = self.env['hr.employee.report'].search([])
        for em in report_ids:
            if em.label == "e. Ít hơn 31 tuổi" or em.label == "f. Từ 31 đến 45 tuổi" \
                    or em.label == "g. Từ 46 đến 55 tuổi" or em.label == "h. Nhiều hơn 55 tuổi":
                self.env['hr.employee.report'].create({
                    'employee_id':
                        em.employee_id.id,
                    'name':
                        '0',
                    'label':
                        '0. Số lượng',
                })

    payslip_count = fields.Integer(compute='_compute_payslip_count', string='Số phiếu lương',
                                   groups="mvb_hr.group_mvb_hr_employee_view,"
                                          " mvb_hr.group_mvb_hr_employee_create,"
                                          "mvb_hr.group_mvb_hr_employee_edit,"
                                          "mvb_hr.group_mvb_hr_employee_delete")


class EthnicGroup(models.Model):
    _name = 'ethnic.group'
    name = fields.Char(string="Name", required=True)
