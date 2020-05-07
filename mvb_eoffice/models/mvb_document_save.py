from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _


class DocumentStorage(models.Model):
    _name = 'mvb.document.save'
    _description = 'Thông tin nhận văn bản'

    human_resources_save = fields.Many2one(comodel_name='res.users', string="Người nhận 111",
                                           domain=[('company_id', '=', 1)])
    department = fields.Char(string="Phòng ban", required=False, related='human_resources_save.mvb_department_name')
    job_name = fields.Char(string="Chức vụ", required=False, related='human_resources_save.mvb_job_name')
    number_save = fields.Integer('Số bản nhận')
    date_save = fields.Date('Ngày nhận')
    type_document_save = fields.Selection(string="Loại văn bản nhận", selection=[('bangoc', 'Bản gốc'),
                                                                                 ('banchinh', 'Bản chính'),
                                                                                 ('bansaoybanchinh',
                                                                                  'Bản sao y bản chính'),
                                                                                 ('banchichsao', 'Bản trích sao'),
                                                                                 ('bansaoluc', 'Bản sao lục'), ])
    save_text_datas_id = fields.Many2one(comodel_name="mvb.incoming.text", string="Văn bản", required=False, )

