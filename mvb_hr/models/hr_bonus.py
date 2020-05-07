from odoo import api, fields, models

class HrBonusType(models.Model):
    _name = 'hr.bonus.type'
    _description = 'Loại khen thưởng'

    name = fields.Char('Tên loại khen thưởng', required=True)

class HrBonus(models.Model):
    _name = 'hr.bonus'
    _description = 'Khen thưởng'

    name = fields.Char(related='employee_id.name', string="Tên")
    year = fields.Char(string="Năm")
    medal = fields.Char(string="Khen thưởng")
    attach_reward_record = fields.Many2many('ir.attachment', 'car_rent_checklist_ir_attachments_rel_bonus',
                                      'rental_id', 'attachment_id', string="Hồ sơ khen thưởng")
    attach_reward_record_name = fields.Char(string="Tên File")
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

    state = fields.Selection(string="Trạng thái", selection=[('draft', 'Nháp'), ('done', 'Hoàn thành')],
                          required=False, default="draft" )

    bonus_type = fields.Many2one(comodel_name="hr.bonus.type", string="Khen thưởng", required=False, )

