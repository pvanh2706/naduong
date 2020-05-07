from odoo import models
from datetime import datetime, date

class MVBContractDocumentXlsx(models.AbstractModel):
    _name = 'report.mvb_documents.mvb_document_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        dict_document = dict()
        for obj in objs:
            if obj.type_contract_document:
                if obj.type_contract_document not in dict_document.keys():
                    dict_document[obj.type_contract_document] = [obj]
                else:
                    dict_document[obj.type_contract_document].append(obj)

        #print(dict_document)
        for key in dict_document.keys():

            sheet = workbook.add_worksheet(key.name)
            bold = workbook.add_format({'bold': True})
            text_wrap = workbook.add_format({
                'text_wrap': True,
                'align': 'center',
                'valign': 'vcenter',
            })
            number_format = workbook.add_format({
                'num_format': '###,###,###',
                'align': 'center',
                'valign': 'vcenter',
            })
            border = workbook.add_format({'border': True})
            center = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter'})
            header_title = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'bold': True,
                'font_size': 14,
            })
            header = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'bold': True,
                'text_wrap': True,
            })

            # set title
            sheet.merge_range("A1:K1", key.name,header_title)

            # set col size

            if not dict_document.get(key)[0].hire_location_pay:
                sheet.set_column('A:A',7)
                sheet.set_column('B:B', 3)
                sheet.set_column('C:C', 20)
                sheet.set_column('D:D', 12)
                sheet.set_column('E:E', 12)
                sheet.set_column('F:F', 12)
                sheet.set_column('G:G', 40)
                sheet.set_column('H:H', 12)
                sheet.set_column('I:I', 12)
                sheet.set_column('J:J', 12)
                sheet.set_column('K:K', 12)
                sheet.set_column('L:L', 12)
                sheet.set_column('M:M', 12)
                sheet.set_column('N:N', 12)
                sheet.set_column('O:O', 14)
                sheet.set_column('Q:Q', 14)
                sheet.set_column('S:S', 14)
                sheet.set_column('P:P', 12)
                sheet.set_column('R:R', 12)

                # write header
                sheet.merge_range("A3:A4", "Quyển", header)
                sheet.merge_range("B3:B4", "", header)
                sheet.merge_range("C3:C4", "Số hiệu hợp đồng", header)
                sheet.merge_range("D3:D4", "Ngày tháng HĐ", header)
                sheet.merge_range('E3:E4', 'Hạn', header)
                sheet.merge_range('F3:F4', 'Thanh lý hợp đồng', header)

                sheet.merge_range("G3:G4", "Nội dung HĐ", header)
                sheet.merge_range("H3:H4", "Đơn vị ký kết", header)
                sheet.merge_range("I3:I4", "ĐVT", header)

                sheet.merge_range('J3:K3',"Giá trị HĐ", header)
                sheet.write('J4',"Sản lượng (tấn)", header)
                sheet.write('K4',"Giá trị (đồng)", header)
                sheet.merge_range('L3:M3',"Giá trị thực hiện HĐ", header)
                sheet.write('L4', "Sản lượng (tấn)", header)
                sheet.write('M4', "Giá trị (đồng)", header)
                sheet.merge_range('N3:O3',"Thời gian HĐ", header)
                sheet.write('N4', "Bắt đầu ", header)
                sheet.write('O4', "Kết thúc thực tế", header)
                sheet.write('P4', "Thanh lý HĐ", header)
                sheet.write("Q3", "Ghi chú", header)

                i = 4
                for line in dict_document.get(key):
                    if line.name:
                        sheet.write(i, 2, line.name, text_wrap)
                    if line.date_contract:
                        sheet.write(i, 3, str(line.date_contract), text_wrap)
                    if line.payment_term:
                        sheet.write(i, 4, str(line.payment_term), text_wrap)
                    if line.tl:
                        sheet.write(i, 5, line.tl, text_wrap)
                    if line.name_document:
                        sheet.write(i, 6, line.name_document, text_wrap)
                    if line.unit_signing:
                        sheet.write(i, 7, line.unit_signing, text_wrap)
                    if line.unit_contract:
                        sheet.write(i, 8, line.unit_contract, text_wrap)

                    sheet.write(i, 9, line.contract_values_quantity, number_format)
                    sheet.write(i, 10, line.contract_values_cost, number_format)

                    sheet.write(i, 11, line.contract_values_action_quantity, number_format)
                    sheet.write(i, 12, line.contract_values_action_cost, number_format)

                    if line.start_contract:
                        sheet.write(i, 13, str(line.start_contract), text_wrap)
                    if line.end_contract:
                        sheet.write(i, 14, str(line.end_contract), text_wrap)
                    if line.liquidation:
                        sheet.write(i, 15, line.liquidation, text_wrap)
                    if line.note_contract:
                        sheet.write(i, 16, line.note_contract, text_wrap)

                    i = i + 1

            else:
                sheet.set_column('A:A', 5)
                sheet.set_column('B:B', 20)
                sheet.set_column('C:C', 12)
                sheet.set_column('D:D', 12)
                sheet.set_column('E:E', 12)
                sheet.set_column('F:F', 35)
                sheet.set_column('G:G', 12)
                sheet.set_column('H:H', 12)
                sheet.set_column('I:I', 12)
                sheet.set_column('J:J', 12)
                sheet.set_column('K:K', 12)
                sheet.set_column('L:L', 12)
                sheet.set_column('M:M', 12)
                sheet.set_column('N:N', 12)
                sheet.set_column('O:O', 14)
                sheet.set_column('Q:Q', 14)
                sheet.set_column('S:S', 14)
                sheet.set_column('P:P', 12)
                sheet.set_column('R:R', 12)

                # write header
                sheet.write("B3", "Số văn bản", header)
                sheet.write("C3", "Ngày VB", header)
                sheet.write("D3", "Hạn", header)
                sheet.write('E3', 'TL', header)
                sheet.write('F3', 'Nội dung', header)

                sheet.write("G3", "Đơn vị ký kết", header)
                sheet.write("H3", "ĐVT", header)
                sheet.write("I3", "Sản lượng", header)

                sheet.write('J3', "Giá trị", header)
                sheet.write('K3', "Vị trí", header)
                sheet.write('L3', "Q", header)
                sheet.write('M3', "Số lg", header)
                sheet.write('N3', "Ghi chú", header)

                i = 3
                for line in dict_document.get(key):
                    if line.name:
                        sheet.write(i, 1, line.name, text_wrap)
                    if line.date_contract:
                        sheet.write(i, 2, str(line.date_contract), text_wrap)
                    if line.payment_term:
                        sheet.write(i, 3, str(line.payment_term), text_wrap)
                    if line.tl:
                        sheet.write(i, 4, line.tl, text_wrap)
                    if line.name_document:
                        sheet.write(i, 5, line.name_document, text_wrap)
                    if line.unit_signing:
                        sheet.write(i, 6, line.unit_signing, text_wrap)
                    if line.unit_contract:
                        sheet.write(i, 7, line.unit_contract, text_wrap)

                    sheet.write(i, 8, line.hire_contract_amount, number_format)
                    sheet.write(i, 9, line.hire_contract_values, number_format)
                    if line.hire_location_pay:
                        sheet.write(i, 10, line.hire_location_pay, text_wrap)
                    if line.q:
                        sheet.write(i, 11, line.q, text_wrap)
                    sheet.write(i, 12, line.hire_contract_number, number_format)

                    if line.note_contract:
                        sheet.write(i, 13, line.note_contract, text_wrap)

                    i = i + 1


