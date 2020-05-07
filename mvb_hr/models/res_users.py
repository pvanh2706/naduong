from odoo import api, fields, models

class UserHR_MVB(models.Model):

    _inherit = 'res.users'

    is_choose = fields.Boolean('Được chọn', default = False)

    mvb_department_name = fields.Char('Phòng ban')
    mvb_job_name = fields.Char('Chức vụ')

    @api.model
    def create(self, values):
        # Add code here
        return super(UserHR_MVB, self).create(values)

    @api.multi
    def name_get(self):
        def _name_get(d):
            name = d.get('name', '')
            project_name = d.get('login_name', False) or ''
            if project_name:
                name = '%s' % (name)
            return (d['id'], name)

        self.check_access_rights("read")
        self.check_access_rule("read")

        result = []
        for mnv in self.sudo():
            mydict = {
                'id': mnv.id,
                'name': mnv.name,
                'login_name': mnv.login,
            }
            result.append(_name_get(mydict))
        return result