from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _


class FormDocumentType(models.Model):
    _name = 'mvb.document.office.type'
    _description = 'Hình thức văn bản'

    name = fields.Char(string="Hình thức văn bản", required=False, )



