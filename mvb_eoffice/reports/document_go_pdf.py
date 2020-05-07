from odoo import api, models, _


class EOfficeReport(models.AbstractModel):
    _name = 'report.mvb_eoffice.document_go_report'
    _description = 'In Văn bản đi dự thảo'

    @api.model
    def _get_report_values(self, docids, data=None):
        print(docids)
        docs = self.env['mvb.draft.text.go'].browse(docids[0])
        print(docs)
        return {
            'doc_model': 'mvb.draft.text.go',
            'docs': docs,
        }
