from odoo import api, fields, models


class EthnicGroup(models.Model):
    _name = 'ethnic.group'

    name = fields.Char(string="Name", required=True)
