from odoo import api, fields, models, _


class ReportInstruction(models.Model):
    _name = 'mvb.waiting.solution'

    _description = 'Giao diện chờ xử lý'

    @api.multi
    def open_patient_appointments(self):
        print('Hello button click')
        return {
            'name': _('Văn bản cần xử lý'),
            'domain': [('state', '=', 'chuaxuly')],
            # 'res_id': self.text_ids.id,
            'view_type': 'form',
            'res_model': 'mvb.people.processing.text',
            # 'view_id': False,
            'view_mode': 'tree',
            'type': 'ir.actions.act_window',
        }

    def get_incoming_count(self):
        self.document_incoming_count = self.env['mvb.people.processing.text'].search_count([])

        # print(self.env['mvb.people.processing.text'].search([]))
    name = fields.Char()
    document_incoming_count = fields.Integer(string="Số văn bản", required=False, compute='get_incoming_count', )
    new_field_id = fields.Many2one(comodel_name="", string="", required=False, )
