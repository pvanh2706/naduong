from odoo import api, fields, models
import time
from odoo.exceptions import UserError, ValidationError, Warning
from odoo.osv import osv
from odoo.tools.translate import _
import datetime

YEAR_NOW_DEFAULT = datetime.datetime.now().year

class MVBDocumentNoteBook(models.Model):
    _name = 'mvb.document.notebook'
    _description = 'Quản lý sổ văn bản'


    type_doc    = fields.Selection([
                                    ('đến','Đến'),
                                    ('đi','Đi'),
                                    ], default='đến', string="Văn bản", store=True)
    year_doc    = fields.Char('Năm', default = YEAR_NOW_DEFAULT,store=True)
    name        = fields.Char('Tên sổ văn bản',readonly=True, store=True)
    _sql_constraints = [
        ('check_name', 'unique(name)', 'Tên sổ văn bản này đã tồn tại. \n Hãy nhập sổ văn bản khác'),
    ]
    @api.onchange('type_doc', 'year_doc')
    def change_info_note(self):
        self.name = 'Sổ văn bản '+ self.type_doc + ' ' + self.year_doc
