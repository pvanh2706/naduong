from odoo import api, fields, models
import re

class HrJob(models.Model):
    _inherit = 'hr.job'

    job_level = fields.Selection(string="Cấp độ nhân viên", selection=[('cbld', 'Cán bộ lãnh đạo'),
                                                           ('cbdt', 'Cán bộ đơn thuần'),
                                                           ('nv', 'Nhân viên'),
                                                           ('cn', 'Công nhân')],

                               required=False, )
    job_position_group = fields.Selection(string="Nhóm chức vụ",
                                          selection=[('jg1', 'Chủ tịch HĐQT, HĐTV, Chủ tịch Công ty'),
                                                     ('jg2', 'Uỷ viên HĐQT, HĐTV'),
                                                     ('jg3', 'Trưởng ban Kiểm soát, Kiểm soát viên trưởng'),
                                                     ('jg4', 'Uỷ viên Ban Kiểm soát, Kiểm soát viên'),
                                                     ('jg5', 'Tổng GĐ, GĐ, hiệu trưởng, viện trưởng'),
                                                     ('jg6', 'Phó TGĐ, Phó GĐ, Phó HT, Phó VT'),
                                                     ('jg7', 'Kế toán trưởng '),
                                                     ('jg8', 'Trưởng phòng, ban, khoa, bộ môn'),
                                                     ('jg9', 'Phó trưởng phòng, ban, khoa, bộ môn'),
                                                     ('jg10', 'Quản đốc và tương đương'),
                                                     ('jg11', 'Phó quản đốc và tương đương'),
                                                     ('jg12', 'Nhân viên hành chính, kỹ thuật, nghiệp vụ'),
                                                     ('jg13', 'Nhân viên phục vụ'),
                                                     ('jg14', 'Công nhân kỹ thuật'),
                                                     ('jg15', 'Công nhân phổ thông')],
                                          required=False, )
    job_position_level = fields.Selection(string="Cấp đơn vị", selection=[('lvl1', 'Đơn vị cấp 1'),
                                                                          ('lvl2', 'Đơn vị cấp 2'),
                                                                          ('lvl3', 'Đơn vị cấp 3'),],
                                          required=False, )

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if not args:
            args = []
        if name:
            positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
            hr_job = self.env['hr.job']
            if operator in positive_operators:
                domain = ['|','|', ('company_id.code', operator, name), ('name', operator, name), ('department_id', operator, name) ]
                hr_job = self.search(
                    domain + args,
                    limit=limit)
            if not hr_job and operator in positive_operators:
                if name.count('[') > 1:
                    new_name = name.split('] ')
                list_data = []
                for rec in new_name:
                    rec = rec.replace('[', '')
                    list_data.append(rec.replace('[', ''))
                if len(list_data) == 3:
                    domain_search = [('company_id.code' , operator, list_data[0]),('department_id.name' , operator, list_data[1]),('name' , operator, list_data[2])]
                    hr_job = self.search(domain_search + args,limit=limit)
        else:
            hr_job = self.search(args, limit=limit)
        return hr_job.name_get()