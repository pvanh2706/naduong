from odoo import api, fields, models
from datetime import datetime


class MVBLeaderDirection(models.Model):
    _name = 'mvb.leadership.direction'
    _description = 'Quản lý chỉ đạo của lãnh đạo'
    _rec_name = 'leadership'

    leadership = fields.Many2one(comodel_name="res.users", string="Chuyển cho lãnh đạo", required=False,
                                 ondelete='cascade')
    content = fields.Text('Nội dung chỉ đạo')
    text_ids = fields.Many2one(comodel_name="mvb.incoming.text", string="Văn bản", required=True, ondelete='cascade')
    date_direction = fields.Datetime(string="Ngày chỉ đạo", required=False, default=fields.Datetime.now)
    dealine_finish = fields.Datetime(string="Thời hạn hoàn thành", required=False, )


class MVBMemberDirection(models.Model):
    _name = 'mvb.member.direction'

    _description = 'Quản lý phân công cho nhân viên'

    member = fields.Many2one(comodel_name="res.users", string="Nhân viên", required=False, )
    position = fields.Char(string="Chức vụ", required=False, readonly=True, store=True)
    date = fields.Datetime(string="Ngày phân công", required=False, default=fields.Datetime.now)
    dealine = fields.Datetime(string="Thời hạn hoàn thành", required=False, )
    # department = fields.Char(string="Phòng ban", required=False, )
    content = fields.Text('Nội dung phân công')
    text_menber_ids = fields.Many2one(comodel_name="mvb.incoming.text", string="Văn bản", required=False,
                                      ondelete='cascade')

    # @api.onchange('member')
    # def add_record(self):
        # self.position = self.env['hr.employee'].search([('user_id', '=', self.member.id)]).job_id.name
        # self.department = self.env['hr.employee'].search([('user_id', '=', self.member.id)]).department_id.name


class MVBLeaderOfficeDirection(models.Model):
    _name = 'mvb.leadership.office.direction'
    _description = 'Quản lý ý kiến chỉ đạo của chánh văn phòng'
    _rec_name = 'leadership_eoffice'

    leadership_eoffice = fields.Many2one(comodel_name="res.users", string="Chuyển cho lãnh đạo", required=False,
                                         ondelete='cascade')
    content_office = fields.Text('Nội dung chỉ đạo')
    office_id = fields.Many2one(comodel_name="mvb.incoming.text", string="Văn bản", required=False, ondelete='cascade')
    date_direction_office = fields.Datetime(string="Ngày chỉ đạo", required=False,
                                            default=fields.Datetime.now)
    dealine_finish_office = fields.Datetime(string="Thời hạn hoàn thành", required=False, )


class ProcessingSolution(models.Model):
    _name = 'mvb.solution.direction'
    _description = 'Quá trình xử lý'
    _rec_name = 'date_start_ship'
    _order = 'date_start_ship desc'

    person_ship = fields.Many2one(comodel_name="res.users", string="Người chuyển", required=False, )
    content_solution = fields.Text('Nội dung')
    solution_id = fields.Many2one(comodel_name="mvb.incoming.text", string="Văn bản", required=False,
                                  ondelete='cascade')
    date_start_ship = fields.Datetime(string="Ngày chuyển", required=False, default=fields.Datetime.now)
    date_deadline = fields.Datetime(string="Hạn xử lý", required=False)

    person_receiver_ids = fields.Many2many(comodel_name="res.users", relation="rel_usera1", column1="r1", column2="r2",
                                           string="Người xử lý chính", )
    person_coordinator_handles_ids = fields.Many2many(comodel_name="res.users", string="Người phối hợp xử lý",
                                                      relation="rel_userb2", column1="r3", column2="r4")
    person_follow_ids = fields.Many2many(comodel_name="res.users", relation="rel_userc3", column1="r5", column2="r6",
                                         string="Người theo dõi văn bản", )
    
    display_name = fields.Char("Người nhận 1", compute='get_display_name')

    @api.multi
    @api.depends('person_receiver_ids')
    def get_display_name(self, type_xxx):
        for rec in self:
            display_name = ''
            count = 0
            print("---------------", rec.person_receiver_ids)
            for user in rec.person_receiver_ids:
                if count < 3:
                    display_name = display_name + user.name + '\n\t\n'
                    count += 1
                else:
                    display_name = display_name + '...'
                    break
            print("va ---------------------------------------", display_name)
           
            rec.update({
                'display_name': display_name,
            })

