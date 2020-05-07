from odoo import api, fields, models
from odoo.osv import expression


class MVBJobAssign(models.Model):
    _name = 'mvb.job_assign'
    _rec_name = 'name'
    _description = 'Công việc được giao'

    name = fields.Char('Tên', compute='_compute_name')
    description = fields.Text('Mô tả công việc')
    user_id = fields.Many2one('res.users', string='Người thực hiện', required=True)
    state = fields.Selection(selection=[('undone','Chưa hoàn thành'),('done', 'Hoàn thành')], string='Trạng thái', default='undone')
    stage = fields.Char('Giai đoạn')
    job_profile_id = fields.Many2one('mvb.job.profiles', string='Thuộc Hồ sơ', required=True)

    @api.one
    @api.depends('job_profile_id', 'user_id')
    def _compute_name(self):
        for em in self:
            if em.job_profile_id and em.user_id:
                em.name = em.job_profile_id.name +' - '+ em.user_id.name

    def to_done(self):
        self.state = 'done'


class MVBJobProfiles(models.Model):
    _name = 'mvb.job.profiles'
    _description = 'Quản lý hồ sơ công việc xử lý văn bản'
    _rec_name = 'name'

    name = fields.Char('Tên', compute='_compute_name')
    description = fields.Text('Nội dung')
    incoming_text_id = fields.Many2one('mvb.incoming.text', string='Văn bản cần xử lý', required=True)
    job_assign_ids = fields.One2many('mvb.job_assign', inverse_name='job_profile_id', string='Danh sách công việc')
    state = fields.Selection(selection=[('undone', 'Chưa hoàn thành'), ('done', 'Hoàn thành')], string='Trạng thái',
                             default='undone', compute='_compute_state')

    @api.one
    @api.depends('incoming_text_id')
    def _compute_name(self):
        for em in self:
            if em.incoming_text_id:
                em.name = 'Hồ sơ xử lý văn bản '+ em.incoming_text_id.name

    @api.one
    @api.depends('job_assign_ids')
    def _compute_state(self):
        for em in self:
            c = 0
            for line in em.job_assign_ids:
                if line.state == 'undone':
                    em.state = 'undone'
                    c = 1
                    break
            if(c == 0):
                em.state = 'done'