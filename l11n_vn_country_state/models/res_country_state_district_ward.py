# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CountryStateDistrict(models.Model):
    _description = "District"
    _name = 'res.country.state.district.ward'
    _order = 'code'

    district_id = fields.Many2one('res.country.state.district', string='District', required=True)
    name = fields.Char(string='Ward', required=True)
    code = fields.Char(string='Ward Code', help='The ward code.', required=True)
    level = fields.Char(string='Level', required=False)
    _sql_constraints = [
        ('name_code_uniq', 'unique(district_id, code)', 'The code of the Ward must be unique by District !')
    ]

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        if self.env.context.get('district_id'):
            args = args + [('district_id', '=', self.env.context.get('district_id'))]
        firsts_records = self.search([('code', '=ilike', name)] + args, limit=limit)
        search_domain = [('name', operator, name)]
        search_domain.append(('id', 'not in', firsts_records.ids))
        records = firsts_records + self.search(search_domain + args, limit=limit)
        return [(record.id, record.display_name) for record in records]
