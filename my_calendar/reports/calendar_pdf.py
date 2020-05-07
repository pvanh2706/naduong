from odoo import api, models, _


class AppointmentReport(models.AbstractModel):
    _name = 'report.my_calendar.calendar_report'
    _description = 'Calendar Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        print(docids)
        docs = self.env['doimoi.total.calendar'].browse(docids[0])
        print(docs)
        return {
            'doc_model': 'doimoi.total.calendar',
            'docs': docs,
        }
