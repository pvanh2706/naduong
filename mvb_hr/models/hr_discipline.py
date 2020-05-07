from odoo import api, fields, models


class HrDiscipline(models.Model):
    _name = 'hr.discipline'
    _description = 'Kỷ luật'

    name = fields.Char(related='employee_id.name', string="Tên")
    year = fields.Char(string='Năm')
    reason = fields.Char(string="Lý do")
    attach_discipline_record = fields.Binary(string="Hồ sơ kỷ luật")
    attach_discipline_record = fields.Many2many('ir.attachment', 'car_rent_checklist_ir_attachments_rel_discipline',
                                            'rental_id', 'attachment_id', string="Hồ sơ khen thưởng")
    attach_discipline_record_name = fields.Char(string="Tên File")
    rules = fields.Selection(string="Luật quy định",
                             selection=[('ld', 'Luật Đảng'),
                                        ('lld', 'Luật lao động'),
                                        ('lcb', 'Luật cán bộ, công chức'),
                                        ('blhs', 'Bộ luật hình sự')])

    method = fields.Selection(string="Hình thức kỷ luật",
                              selection=[('kt', 'Khiển trách'),
                                         ('cc', 'Cảnh cáo'),
                                         ('cc1', 'Cách chức'),
                                         ('ld', 'Lưu Đảng'),
                                         ('kt1', 'Khai trừ'),
                                         ('kd', 'Kéo dài thời hạn nâng lương'),
                                         ('cv', 'Chuyển việc khác, hạ lương'),
                                         ('st', 'Sa thải'), ('hl', 'Hạ lương'),
                                         ('ct', 'Cải tạo'), ('qc', 'Quản chế'),
                                         ('tg', 'Tự gieo'), ('tg1', 'Tự giam'),
                                         ('th', 'Tử hình')])

    employee_id = fields.Many2one(string='Nhân viên',
                                  comodel_name='hr.employee',
                                  required=True, ondelete='cascade')
    company_id = fields.Many2one(string="Công ty",
                                 related="employee_id.company_id",
                                 store=True)
    department_id = fields.Many2one(related='employee_id.department_id',
                                    string='Phòng ban',
                                    readonly=True)
    job_id = fields.Many2one(related='employee_id.job_id',
                                    string='Chức vụ',
                                    readonly=True)
