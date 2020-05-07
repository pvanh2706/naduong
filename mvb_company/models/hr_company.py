from odoo import api, fields, models
from odoo.osv import expression
import re


class Company(models.Model):
    _inherit = 'res.company'

    is_corporation = fields.Boolean(string='Là Tổng công ty?', default=False)
    code = fields.Char(string='Mã công ty')


    @api.multi
    def name_get(self):
        def _name_get(d):
            name = d.get('name', '')
            code = d.get('code', False) or ''
            if code:
                name = '[%s] %s' % (code, name)
            return (d['id'], name)

        self.check_access_rights("read")
        self.check_access_rule("read")

        result = []
        for com in self.sudo():
            mydict = {
                'id': com.id,
                'name': com.name,
                'code': com.code,
            }
            result.append(_name_get(mydict))
        return result

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        if not args:
            args = []
        if name:
            positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
            coms = []
            if operator in positive_operators:
                coms = self._search([('code', '=', name)] + args, limit=limit, access_rights_uid=name_get_uid)
                # if not product_ids:
                #     product_ids = self._search([('barcode', '=', name)] + args, limit=limit, access_rights_uid=name_get_uid)
            if not coms and operator not in expression.NEGATIVE_TERM_OPERATORS:
                # Do not merge the 2 next lines into one single search, SQL search performance would be abysmal
                # on a database with thousands of matching products, due to the huge merge+unique needed for the
                # OR operator (and given the fact that the 'name' lookup results come from the ir.translation table
                # Performing a quick memory merge of ids in Python will give much better performance
                coms = self._search(args + [('code', operator, name)], limit=limit)
                if not limit or len(coms) < limit:
                    # we may underrun the limit because of dupes in the results, that's fine
                    limit2 = (limit - len(coms)) if limit else False
                    product2_ids = self._search(args + [('name', operator, name), ('id', 'not in', coms)], limit=limit2, access_rights_uid=name_get_uid)
                    coms.extend(product2_ids)
            elif not coms and operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = expression.OR([
                    ['&', ('code', operator, name), ('name', operator, name)],
                    ['&', ('code', '=', False), ('name', operator, name)],
                ])
                domain = expression.AND([args, domain])
                coms = self._search(domain, limit=limit, access_rights_uid=name_get_uid)
            if not coms and operator in positive_operators:
                ptrn = re.compile('(\[(.*?)\])')
                res = ptrn.search(name)
                if res:
                    coms = self._search([('code', '=', res.group(2))] + args, limit=limit, access_rights_uid=name_get_uid)
            # still no results, partner in context: search on supplier info as last hope to find something

        else:
            coms = self._search(args, limit=limit, access_rights_uid=name_get_uid)
        return self.browse(coms).name_get()

    @api.onchange('is_corporation')
    def _onchange_is_corporation(self):
        for en in self:
            if en.is_corporation:
                en.code = "Tổng công ty"
