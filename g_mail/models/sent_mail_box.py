# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SentGmail(models.Model):
    _name = 'g_mail.sent_mail'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Quản lý Mail đến'

    name = fields.Char(string="Chủ Đề", required=True, )
    partner_ids = fields.Many2many(
        'res.partner', 'mail_outgoing_res_partner_rel',
        'wizard_id', 'partner_id', 'Người nhận')
    outgoing_date = fields.Datetime(string="Ngày nhận", required=False, default=fields.Datetime.now)
    # mail_from = fields.Char(string="Mail", required=False, related="partner_id.email")
    content = fields.Html(string="Nội dung", )
    state = fields.Selection([
        ('draft', 'Chưa gửi'),
        ('confirm', 'Đã gửi'),
    ], string='Status', readonly=True, track_visibility='onchange', copy=False, default='draft',
        help="")

    def outgoing_send_email(self):
        form_view_id = self.env.ref('mail.email_compose_message_wizard_form').id
        return {
            'name': 'Soạn thư',
            'type': 'ir.actions.act_window',
            'res_model': 'mail.compose.message',
            'context': "{'default_sent_mail': active_id}",
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': form_view_id,
            'target': 'new',
        }


