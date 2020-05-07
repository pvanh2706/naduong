# # Copyright 2017 Creu Blanca
# # License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
#
# from odoo import models
#
#
# class PartnerXlsx(models.AbstractModel):
#     _name = 'report.mvb_hr_payroll.payslip_run_xlsx'
#     _inherit = 'report.report_xlsx.abstract'
#
#     def generate_xlsx_report(self, workbook, data, runs):
#         for obj in runs:
#             sheet = workbook.add_worksheet('Report')
#             bold = workbook.add_format({'bold': True})
#             sheet.write(0, 0, obj.name, bold)
