# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.exceptions import UserError, ValidationError


class checkRangeDate(models.TransientModel):
    _name = 'mvb.range.date'
    _description = 'Lọc bản ghi theo thời gian'

    name = fields.Char(string="Tên", required=False, )
    start_date = fields.Date('Thời gian bắt đầu', required=True)
    end_date = fields.Date('Thời gian kết thúc', required=True)
    state = fields.Selection(string="Trạng thái",
                             selection=[('draft', 'Đã vào sổ'), ('pending', 'Đang xử lý'), ('finish', 'Kết thúc')],
                             required=False, default="draft")

    @api.multi
    @api.constrains('start_date', 'end_date')
    def check_date(self):
        if self.end_date < self.start_date:
            raise ValidationError("Ngày kết thúc phải lớn hơn ngày bắt đầu")

    def filter_space_date(self):
        print('test')
        domain = [('received_date', '>', self.start_date), ('received_date', '<', self.end_date)]
        # res = self.env['mvb.incoming.text'].search(domain)
        # if res:
        #     print('test')
        # tree_view_id = self.env.ref('mvb_eoffice.mvb_text_to_come_action').id
        return {
                'name': _('Văn bản đến'),
                'domain': domain,
                'view_type': 'form',
                'res_model': 'mvb.incoming.text',
                'view_id': False,
                'view_mode': 'tree,form',
                'type': 'ir.actions.act_window',
            }

