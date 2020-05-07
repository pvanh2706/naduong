from odoo import api, fields, models
from odoo.osv import expression
import re


class HrDepartment(models.Model):
    _inherit = 'hr.department'

    _sql_constraints = [
        ('name_company_uniq', 'unique (name, company_id)', 'Đã tồn tại phòng ban này trong công ty!')
    ]

    @api.multi
    def name_get(self):
        def _name_get(d):
            name = d.get('name', '')
            company_id = self._context.get('company_id', True) and d.get(
                'company_id', False) or False
            # code = self._context.get('department_code', True) and d.get(
            #     'department_code', False) or False
            # if code:
            #     name = '[%s] [%s] %s' % (company_id, code, name)
            if company_id:
                name = '[%s] %s' % (company_id, name)
            return (d['id'], name)

        self.check_access_rights("read")
        self.check_access_rule("read")

        result = []
        for depart in self.sudo():
            mydict = {
                'id': depart.id,
                'name': depart.name,
                'company_id': depart.company_id.code,
                # 'department_code': employee.department_code,
            }
            result.append(_name_get(mydict))
        return result

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if not args:
            args = []
        if name:
            positive_operators = ['=', 'ilike', '=ilike', 'like', '=like']
            hr_department = self.env['hr.department']
            if operator in positive_operators:
                hr_department = self.search(
                    [('company_id.code', '=', name)] + args,
                    limit=limit)
            if not hr_department and operator in positive_operators:
                ptrn = re.compile('(\[(.*?)\])')
                res = ptrn.search(name)
                if res:
                    name_resource = name.split(']')[1].strip()
                    value1 = len(name_resource)
                    value2 = len(res.group(1))
                    if (value1 < 1) and (value2 > 0):
                        hr_department = self.search(
                            [('company_id.code', operator, res.group(2))] + args,
                            limit=limit)
                    elif (value2 < 1) and (value1 > 0):
                        hr_department = self.search(
                            [
                                ('name', operator, name_resource)
                            ] + args,
                            limit=limit)
                    elif (value2 > 0) and (value1 > 0):
                        hr_department = self.search(
                            ['&',
                             ('company_id.code', operator, res.group(2)), ('name', operator, name_resource)
                             ] + args,
                            limit=limit)
        else:
            hr_department = self.search(args, limit=limit)
        return hr_department.name_get()
