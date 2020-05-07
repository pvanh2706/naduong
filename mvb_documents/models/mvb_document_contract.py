from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _

class MVBDocumentContractType(models.Model):
    _name = 'mvb.document.contract.type'
    _description = 'Quản lý danh sách loại hợp đồng'

    name = fields.Char('Loại hợp đồng', required=True)