from odoo import api, fields, models, _
from odoo.exceptions import UserError


class HrTrainingReportGenProperty(models.TransientModel):
    _name = 'training.report.gen_property'
    _description = 'Tạo dòng báo cáo theo tiêu chí'

    property_ids = fields.Many2many( 'train.plan.property', string='Tiêu chí')

    @api.multi
    def generate(self):
        [data] = self.read()
        active_id = self.env.context.get('active_id')

        if not data['property_ids']:
            raise UserError(_("Bạn phải chọn tiêu chí để tạo báo cáo."))
        ls_property_ids = data['property_ids']
        ls_line = self.env['train.property.report'].search(
            [('report_id', '=', active_id), ('property_id', 'in', ls_property_ids)])
        dict_line = {line.property_id.id: line for line in ls_line}
        for pro in self.env['train.plan.property'].browse(ls_property_ids):
            line_in_db = dict_line.get(pro.id)
            if line_in_db:
                continue

            res = {
                'property_id': pro.id,
                'report_id': active_id,

            }
            self.env['train.property.report'].create(res)

        return {'type': 'ir.actions.act_window_close'}
