from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.translate import _

class TextCodeStorage(models.Model):
    _inherit = 'mvb.document.storage'

    storage_text_datas = fields.Many2one(comodel_name="mvb.text", string="Văn bản", required=False, )