from odoo import api, fields, models


class HrStudyProcess(models.Model):
    _name = "hr.study.process"
    _rec_name = 'name_school'

    name_school = fields.Char(string="Tên trường")
    major = fields.Char(string="Ngành học và tên lớp học")
    date = fields.Char(string="Thời gian học")
    formality = fields.Char(string="Hình thức học", help="Chính quy, tại chức, chuyên tu, bồi dưỡng, mở rộng")
    certificate = fields.Char(string="Văn bằng, chứng chỉ, trình độ gì", help="tiến sỹ, thạc sỹ, cử nhân, kỹ sư...")

    employee_id = fields.Many2one(string="Nhân viên", comodel_name="hr.employee", required=True, ondelete='cascade')
