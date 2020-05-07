# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
import datetime


class DashBoardAction(models.TransientModel):
    _name = 'dash.board.action.wizards'
    _description = 'Màn hình giao diện công việc chờ xử lý'

    def _count_incoming_solution(self):
        document_now = datetime.datetime.now()
        res = self.env['mvb.people.processing.text'].search_count(
            [('name', '=', self._uid), ('check_work', '=', False), ('state', '!=', 'theodoi')])
        return res

    def _count_incoming_deadline(self):

        document_now = datetime.datetime.now()
        res = self.env['mvb.people.processing.text'].search_count(
            [('name', '=', self._uid), ('check_work', '=', False), ('deadline', '<', document_now)])
        return res

    def _count_incoming_follow(self):
        res = self.env['mvb.people.processing.text'].search_count([('state', '=', 'theodoi'), ('name', '=', self._uid)])
        return res

    def _count_document_notification(self):
        res = self.env['mvb.incoming.text'].search_count([('state', '=', 'notification')])
        return res

    def _count_outgoing_solution(self):
        res = self.env['mvb.people.processing.textdraft'].search_count(
            [('state', '=', 'chuaxuly'), ('name', '=', self._uid)])
        return res

    def _count_document_outgoing_deadline(self):
        document_now = datetime.datetime.now()
        res = self.env['mvb.people.processing.textdraft'].search_count(
            [('state', '=', 'chuaxuly'), ('name', '=', self._uid), ('dead_line', '<', document_now)])
        return res

    def count_document_text_incoming(self):
        res = self.env['mvb.incoming.text'].search_count(
            ['|', ('create_uid', '=', self._uid), ('status_text.name.id', '=', self._uid)])
        return res

    def count_document_text_outgoing(self):
        res = self.env['mvb.text.go'].search_count(['|', ('member.id', '=', self._uid), ('create_uid', '=', self._uid)])
        return res

    def _view_calendar(self):
        res = self.env['doimoi.total.calendar'].search([('state', '=', 'confirm')], limit=1, order='date_from DESC')
        if res:
            calendar_Html = '<h2 style="text-align: center; color: white; background-color: #5D8DA8; padding: 2px;">LỊCH CÔNG TÁC %s </br><small>(Từ %s đến %s)</small></h2>' % (
                res.name.upper(), res.date_from.strftime('%d/%m/%Y'),
                res.date_to.strftime('%d/%m/%Y')) + '</br>' + res.calendar
        else:
            calendar_Html = '</br>'
        return calendar_Html

    def name(self):
        res = 'Bảng tổng hợp'
        return res

    name = fields.Char(string="", required=False, default=name)
    count_incoming_solution = fields.Integer(string="Văn bản đến cần xử lý", required=False,
                                             default=_count_incoming_solution)

    count_incoming_follow = fields.Integer(string="Văn bản đến theo dõi", required=False,
                                           default=_count_incoming_follow)
    count_document_deadline = fields.Integer(string="Văn bản quá hạn xử lý", required=False,
                                             default=_count_incoming_deadline)
    count_document_notification = fields.Integer(string="Văn bản thông báo", required=False,
                                                 default=_count_document_notification)
    count_outgoing_solution = fields.Integer(string="Văn bản dự thảo chờ xử lý", required=False,
                                             default=_count_outgoing_solution)
    count_document_outgoing_deadline = fields.Integer(string="Văn bản dự thảo quá hạn xử lý", required=False,
                                                      default=_count_document_outgoing_deadline)
    count_document_text_incoming = fields.Integer(string="Số văn bản đến", required=False,
                                                  default=count_document_text_incoming)
    count_document_text_outgoing = fields.Integer(string="Số văn bản đi", required=False,
                                                  default=count_document_text_outgoing)
    view_calendar = fields.Html(string="Lịch công tác tuần", default=_view_calendar, readonly=True)

    @api.model
    def default_get(self, fields):
        res = super(DashBoardAction, self).default_get(fields)
        return res

    def action_document_incoming(self):
        return {
            'name': _('Văn bản đến chờ xử lý'),
            'domain': [('name', '=', self._uid), ('check_work', '=', False), ('state', '!=', 'theodoi')],
            'view_type': 'form',
            'res_model': 'mvb.people.processing.text',
            # 'view_id': False,
            'view_mode': 'tree',
            'type': 'ir.actions.act_window',
        }

    def action_document_incoming_deadline(self):
        document_now = datetime.datetime.now()
        return {
            'name': _('Văn bản đến chờ xử lý'),
            'domain': [('name', '=', self._uid), ('check_work', '=', False), ('state', '!=', 'theodoi'),
                       ('deadline', '<', document_now)],
            'view_type': 'form',
            'res_model': 'mvb.people.processing.text',
            # 'view_id': False,
            'view_mode': 'tree',
            'type': 'ir.actions.act_window',
        }

    def action_document_follow(self):
        return {
            'name': _('Văn bản đến đang theo dõi'),
            'domain': [('name', '=', self._uid), ('state', '=', 'theodoi')],
            'view_type': 'form',
            'res_model': 'mvb.people.processing.text',
            # 'view_id': False,
            'view_mode': 'tree',
            'type': 'ir.actions.act_window',
        }

    def action_document_notification(self):
        return {
            'name': _('Văn bản thông báo'),
            'domain': [('state', '=', 'notification')],
            'view_type': 'form',
            'res_model': 'mvb.incoming.text',
            # 'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def action_document_outgoing(self):
        return {
            'name': _('Văn bản đi dự thảo chờ xử lý'),
            'domain': [('name', '=', self._uid), ('state', '=', 'chuaxuly')],
            'view_type': 'form',
            'res_model': 'mvb.people.processing.textdraft',
            # 'view_id': False,
            'view_mode': 'tree',
            'type': 'ir.actions.act_window',
        }

    def action_document_outgoing_deadline(self):
        document_now = datetime.datetime.now()
        return {
            'name': _('Văn bản đi dự thảo chờ xử lý'),
            'domain': [('name', '=', self._uid), ('state', '=', 'chuaxuly'), ('dead_line', '<', document_now)],
            'view_type': 'form',
            'res_model': 'mvb.people.processing.textdraft',
            # 'view_id': False,
            'view_mode': 'tree',
            'type': 'ir.actions.act_window',
        }

    def action_document_incoming_for_person(self):
        return {
            'name': _('Văn bản đến'),
            'domain': ['|', ('create_uid', '=', self._uid), ('status_text.name.id', '=', self._uid)],
            'view_type': 'form',
            'res_model': 'mvb.incoming.text',
            # 'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }

    def action_document_outgoing_for_person(self):
        return {
            'name': _('Văn bản đi'),
            'domain': ['|', ('member.id', '=', self._uid), ('create_uid', '=', self._uid)],
            'view_type': 'form',
            'res_model': 'mvb.text.go',
            # 'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }
