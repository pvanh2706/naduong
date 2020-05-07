# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.http import request
from odoo.exceptions import UserError


class Gmail(models.Model):
    _name = 'g_mail.mailbox'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Quản lý Mail đến'

    name = fields.Char(string="Chủ Đề", required=False, )
    partner_id = fields.Many2one(comodel_name="res.partner", string="Người gửi", required=False, )
    incoming_date = fields.Datetime(string="Ngày nhận", required=False, default=fields.Datetime.now)
    mail_from = fields.Char(string="Mail", required=False, related="partner_id.email")
    content = fields.Html(string="Nội dung", )

    state = fields.Selection([
        ('draft', 'Chờ vào sổ'),
        ('confirm', 'Đã vào sổ'),
    ], string='Status', readonly=True, track_visibility='onchange', copy=False, default='draft',
        help="")

    def reply(self):
        self.state = 'draft'

    def create_incoming_text(self):
        self = self.sudo()
        if self:
            # self.state = 'confirm'
            form_view_id = self.env.ref('mvb_eoffice.mvb_text_to_come_form_view').id
            return {
                'name': 'Văn bản đến',
                'type': 'ir.actions.act_window',
                'res_model': 'mvb.incoming.text',
                'context': "{'default_email_incoming_text_id': active_id}",
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': form_view_id,
                'target': 'new',
            }

    @api.model
    def create(self, values):
        print(values)
        return super(Gmail, self).create(values)


