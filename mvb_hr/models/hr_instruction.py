from odoo import api, fields, models


class HrInstruction(models.Model):
    _name = 'hr.instruction'
    _rec_name = 'name'
    _description = 'Hướng dẫn sử dụng module nhân sự'

    name = fields.Char()
