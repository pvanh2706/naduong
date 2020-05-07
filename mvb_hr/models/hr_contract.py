from odoo import api, fields, models


class HrDocumentType(models.Model):
    _name = 'hr.document.type'

    name = fields.Char('Name')
    description = fields.Char('Mô tả')


class ContractDocument(models.Model):
    _name = 'hr.document'

    name = fields.Char('Name')
    document_code = fields.Char('Số hiệu VB')
    create_date = fields.Char('Ngày VB')
    expired_date = fields.Char('Hiệu lực VB')
    type_of_document = fields.Many2one('hr.document.type', string='Loại VB')
    storage_place = fields.Char('Nơi lưu trữ VB')
    employee_id = fields.Many2one('hr.employee', 'Nhân sự lưu trữ VB')
    employee_id2 = fields.Many2one('hr.employee', 'Nhân sự lưu trữ VB')
    employee_id3 = fields.Many2one('hr.employee', string='chủ văn bản, tài liệu')
    number_of_document = fields.Integer('Số lượng bản lưu')
    other_file = fields.Binary("Đính kèm")
    contract_id = fields.Many2one('hr.contract', 'Contract')
    position_history_id = fields.Many2one('hr.position.history', 'Position History')
    certification_agency = fields.Char(string="Cơ quan cấp")
    other_file_name = fields.Char("Tên file")

class HrContract(models.Model):
    _inherit = 'hr.contract'

    contract_document_ids = fields.One2many(comodel_name="hr.document", inverse_name="contract_id",
                                            string="Contract Documents")
