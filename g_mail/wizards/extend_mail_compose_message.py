# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ExtendMailComposer(models.TransientModel):
    _inherit = 'mail.compose.message'

    sent_mail = fields.Many2one(comodel_name="g_mail.sent_mail", string="Gửi mail", )

    # mvb_text_go = fields.Many2one(comodel_name="mvb_eoffice.mvb.text.go", string="Gửi mail", required=True, )

    @api.multi
    @api.onchange('template_id')
    def onchange_template_id_wrapper(self):
        self.ensure_one()
        values = self.onchange_template_id(self.template_id.id, self.composition_mode, self.model, self.res_id)['value']
        for fname, value in values.items():
            setattr(self, fname, value)
        res = self.env['mvb.text.go'].browse(self._context.get('active_id'))
        if res:
            res_attachment_ids = self.env['ir.attachment'].search(
                [('res_id', '=', res.id), ('res_model', '=', 'mvb.text.go')])
            if res_attachment_ids:
                self.attachment_ids = res_attachment_ids
        print('test_toan')
        if self.sent_mail:
            rec = self.sent_mail
            rec_attachment_ids = self.env['ir.attachment'].search(
                [('res_id', '=', rec.id), ('res_model', '=', 'g_mail.sent_mail')])
            if rec_attachment_ids:
                self.attachment_ids = rec_attachment_ids
            self.partner_ids = rec.partner_ids
            self.body = rec.content
            self.subject = rec.name

    @api.multi
    def action_send_mail(self):
        rec = self.env['g_mail.sent_mail'].browse(self._context.get('active_id'))
        if rec:
            rec.write({'state': 'confirm'})
        self.send_mail()
        return {'type': 'ir.actions.act_window_close', 'infos': 'mail_sent'}
