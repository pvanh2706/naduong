from odoo import models
from datetime import datetime, date


class ReportHrDisciplinedXlsx(models.AbstractModel):
    _name = 'report.mvb_hr.disciplined_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        for obj in objs:
            sheet = workbook.add_worksheet('Năm ' + str(obj.year))
            bold = workbook.add_format({'bold': True, 'border': True})
            text_wrap = workbook.add_format({
                'text_wrap': True,
                'align': 'center',
                'valign': 'vcenter',
                'border': True
            })
            property_1 = workbook.add_format({
                'bold': True,
                'border': True
            })
            number_format = workbook.add_format({
                'num_format': '###,###,###', 'border': True
            })
            border = workbook.add_format({'border': True})
            no_border = workbook.add_format({'border': False})
            center = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'border': True})
            header_title = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'font_size': 10,
                'text_wrap': True,
                'border': True
            })
            header_main_title = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'bold': True,
                'font_size': 12,
                'text_wrap': True,
                'border': True,
                'underline': True
            })
            header_main_title_bc = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'bold': True,
                'font_size': 12,
                'font': 'Times New Roman'
            })
            stt = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                "border": True})
            stt_bold = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'bold' : True,
                "border": True})
            header = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'border': True,
                'text_wrap': True,
                'font_size': 12,
                'font': 'Times New Roman'
            })

            # set title
            sheet.write("M1","BÁO CÁO XỬ LÝ KỶ LUẬT CÁN BỘ",header_main_title_bc)
            sheet.write("A1","TẬP ĐOÀN CÔNG NGHIỆP",header_main_title_bc)
            sheet.write("A2","THAN KHOÁNG SẢN VIỆT NAM",header_main_title_bc)
            sheet.write("M2", "Sáu tháng đầu năm, sáu tháng cuối năm và cả năm", header_main_title_bc)
            sheet.write("V1","BC: 04/TCCB",header_main_title_bc)
            sheet.write("Z2","Ngày nộp: 15/7 và 15/01 năm sau",header_main_title_bc)
            sheet.write("Z3","Nơi nhận: Ban TCCB Tập đoàn",header_main_title_bc)
            sheet.write("E5"," ",header_main_title)
            sheet.write("B5", " ", header_main_title)

            sheet.merge_range("A5:A10", "CHỨC DANH BỊ XỬ LÝ KỶ LUẬT", header)
            sheet.merge_range("B5:B10", "Tổng số", header)
            sheet.merge_range("C5:D5", "Trong kỳ", header)
            sheet.merge_range("C6:C10", "Đảng viên", header)
            sheet.merge_range("D6:D10", "Phụ nữ", header)
            sheet.merge_range("E6:E10", "Lý do bị xử lý kỷ luật (tóm tắt)", header)
            sheet.merge_range("F5:Z5", "HÌNH THỨC XỬ LÝ", header)
            sheet.merge_range("F6:J6", "Kỷ luật Đảng", header)
            sheet.merge_range("K6:O6", "KL theo Luật lao động", header)
            sheet.merge_range("P6:U6", "KL theo Luật cán bộ, công chức", header)
            sheet.merge_range("V6:Z6", "Xử lý theo bộ luật hình sự", header)
            sheet.merge_range("F7:F10", "Khiển trách", header)
            sheet.merge_range("G7:G10", "Cảnh cáo", header)
            sheet.merge_range("H7:H10", "Cách chức", header)
            sheet.merge_range("I7:I10", "Lưu đảng", header)
            sheet.merge_range("J7:J10", "Khai trừ", header)
            sheet.merge_range("K7:K10", "Khiển trách", header)
            sheet.merge_range("L7:L10", "Kéo dài thời hạn nâng lương", header)
            sheet.merge_range("M7:M10", "Chuyển việc khác, hạ lương", header)
            sheet.merge_range("N7:N10", "Cách chức", header)
            sheet.merge_range("O7:O10", "Sa thải", header)
            sheet.merge_range("P7:P10", "Khiển trách", header)
            sheet.merge_range("Q7:Q10", "Cảnh cáo", header)
            sheet.merge_range("R7:R10", "Hạ lương", header)
            sheet.merge_range("S7:S10", "Hạ ngạch", header)
            sheet.merge_range("T7:T10", "Cách chức", header)
            sheet.merge_range("U7:U10", "Buộc thôi việc", header)
            sheet.merge_range("V7:V10", "Cải tạo", header)
            sheet.merge_range("W7:W10", "Quản chế", header)
            sheet.merge_range("X7:X10", "Tự treo", header)
            sheet.merge_range("Y7:Y10", "Tự giam", header)
            sheet.merge_range("Z7:Z10", "Tử hình", header)

            list_header = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R','S','T','U','V','W','X','Y','Z']
            
            index_header = 11
            id_index = 1
            for i in list_header:
                sheet.write(i+str(index_header),str(id_index),header_main_title)
                id_index = id_index + 1

            lists_header = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R','S','T','U','V','W','X','Y','Z']
            col = 0
            c = 1
            n = 24
            sheet.write('A48',"Cộng (a+b+c)",bold)
            for i in range(1,25):
                for c in range(24):
                    if c <= n:
                        sheet.write(47, col + i, "=SUM("+ lists_header[i] + str(12) + "," 
                                                        + lists_header[i] + str(24) + "," 
                                                        + lists_header[i] + str(36) + ")", number_format)


            # set col size
            sheet.set_column('A:A', 60, no_border)
            sheet.set_column('B:B', 15, no_border)
            sheet.set_column('E:E', 40, no_border)

            list_sub_pro = []
            list_1_level_sub_pro = []
            amount_dict = dict()

            # get value from report
            for line in obj.line_ids:
                list_sub_t = []
                for li in line.property_id.property_ids:
                    list_sub_t.append(li)
                    s = '|'.join(map(str, list_sub_t))
                    if s not in amount_dict.keys():
                        new_dict = dict()
                        new_dict['total'] = line.total
                        new_dict['in_period_communist_mem'] = line.in_period_communist_mem
                        new_dict['in_period_women'] = line.in_period_women
                        new_dict['discipline_reason'] = line.discipline_reason
                        new_dict['kld_khientrach'] = line.kld_khientrach
                        new_dict['kld_canhcao'] = line.kld_canhcao
                        new_dict['kld_cachchuc'] = line.kld_cachchuc
                        new_dict['kld_luudang'] = line.kld_luudang
                        new_dict['kld_khaitru'] = line.kld_khaitru
                        new_dict['lld_khientrach'] = line.lld_khientrach
                        new_dict['lld_keodai'] = line.lld_keodai
                        new_dict['lld_chuyenviec'] = line.lld_chuyenviec
                        new_dict['lld_khaitru'] = line.lld_khaitru
                        new_dict['lld_sathai'] = line.lld_sathai
                        new_dict['lcb_khientrach'] = line.lcb_khientrach
                        new_dict['lcb_canhcao'] = line.lcb_canhcao
                        new_dict['lcb_haluong'] = line.lcb_haluong
                        new_dict['lcb_hangach'] = line.lcb_hangach
                        new_dict['lcb_cachchuc'] = line.lcb_cachchuc
                        new_dict['lcb_thoiviec'] = line.lcb_thoiviec
                        new_dict['lhs_caitao'] = line.lhs_caitao
                        new_dict['lhs_quanche'] = line.lhs_quanche
                        new_dict['lhs_tutreo'] = line.lhs_tutreo
                        new_dict['lhs_tugiam'] = line.lhs_tugiam
                        new_dict['lhs_tuhinh'] = line.lhs_tuhinh
                        amount_dict [s] = new_dict
                    else:
                        amount_dict.get(s)['total'] = amount_dict.get(s)['total'] + line.total
                        amount_dict.get(s)['in_period_communist_mem'] = amount_dict.get(s)['in_period_communist_mem'] + line.in_period_communist_mem
                        amount_dict.get(s)['in_period_women'] = amount_dict.get(s)['in_period_women'] + line.in_period_women
                        amount_dict.get(s)['discipline_reason'] = amount_dict.get(s)['discipline_reason']
                        amount_dict.get(s)['kld_khientrach'] = amount_dict.get(s)['kld_khientrach'] + line.kld_khientrach
                        amount_dict.get(s)['kld_canhcao'] = amount_dict.get(s)['kld_canhcao'] + line.kld_canhcao
                        amount_dict.get(s)['kld_cachchuc'] = amount_dict.get(s)['kld_cachchuc'] + line.kld_cachchuc
                        amount_dict.get(s)['kld_luudang'] = amount_dict.get(s)['kld_luudang'] + line.kld_luudang
                        amount_dict.get(s)['kld_khaitru'] = amount_dict.get(s)['kld_khaitru'] + line.kld_khaitru
                        amount_dict.get(s)['lld_khientrach'] = amount_dict.get(s)['lld_khientrach'] + line.lld_khientrach
                        amount_dict.get(s)['lld_keodai'] = amount_dict.get(s)['lld_keodai'] + line.lld_keodai
                        amount_dict.get(s)['lld_chuyenviec'] = amount_dict.get(s)['lld_chuyenviec'] + line.lld_chuyenviec
                        amount_dict.get(s)['lld_khaitru'] = amount_dict.get(s)['lld_khaitru'] + line.lld_khaitru
                        amount_dict.get(s)['lld_sathai'] = amount_dict.get(s)['lld_sathai'] + line.lld_sathai
                        amount_dict.get(s)['lcb_khientrach'] = amount_dict.get(s)['lcb_khientrach'] + line.lcb_khientrach
                        amount_dict.get(s)['lcb_canhcao'] = amount_dict.get(s)['lcb_canhcao'] + line.lcb_canhcao
                        amount_dict.get(s)['lcb_haluong'] = amount_dict.get(s)['lcb_haluong'] + line.lcb_haluong
                        amount_dict.get(s)['lcb_hangach'] = amount_dict.get(s)['lcb_hangach'] + line.lcb_hangach
                        amount_dict.get(s)['lcb_cachchuc'] = amount_dict.get(s)['lcb_cachchuc'] + line.lcb_cachchuc
                        amount_dict.get(s)['lcb_thoiviec'] = amount_dict.get(s)['lcb_thoiviec'] + line.lcb_thoiviec
                        amount_dict.get(s)['lhs_caitao'] = amount_dict.get(s)['lhs_caitao'] + line.lhs_caitao
                        amount_dict.get(s)['lhs_quanche'] = amount_dict.get(s)['lhs_quanche'] + line.lhs_quanche
                        amount_dict.get(s)['lhs_tutreo'] = amount_dict.get(s)['lhs_tutreo'] + line.lhs_tutreo
                        amount_dict.get(s)['lhs_tugiam'] = amount_dict.get(s)['lhs_tugiam'] + line.lhs_tugiam
                        amount_dict.get(s)['lhs_tuhinh'] = amount_dict.get(s)['lhs_tuhinh'] + line.lhs_tuhinh

                    if li.id not in list_sub_pro:
                        list_sub_pro.append(li.id)
                    if li not in list_1_level_sub_pro and li.level == 1:
                        list_1_level_sub_pro.append(li)

            def sortSecond(val):
                return val.sequence
            list_1_level_sub_pro.sort(key = sortSecond)

            def print_property(list, index, list_t):
                for line in list:

                    list_tc = list_t.copy()
                    list_tc.append(line)
                    s = '|'.join(map(str, list_tc))
                    
                    if s in amount_dict.keys():
                        sheet.write(index, 1, line.name,border)

                        discipline_reason_text = ''
                        if str(amount_dict.get(s).get('discipline_reason')) != 'False':
                            discipline_reason_text = str(amount_dict.get(s).get('discipline_reason'))
                        sheet.write(index, 0, line.name, border)
                        # write values of this row
                        sheet.write(index, 1, amount_dict.get(s).get('total'), number_format)
                        sheet.write(index, 2, amount_dict.get(s).get('in_period_communist_mem'), number_format)
                        sheet.write(index, 3, amount_dict.get(s).get('in_period_women'), number_format)
                        sheet.write(index, 4, discipline_reason_text, text_wrap)
                        sheet.write(index, 5, amount_dict.get(s).get('kld_khientrach'), number_format)
                        sheet.write(index, 6, amount_dict.get(s).get('kld_canhcao'), number_format)
                        sheet.write(index, 7, amount_dict.get(s).get('kld_cachchuc'), number_format)
                        sheet.write(index, 8, amount_dict.get(s).get('kld_luudang'), number_format)
                        sheet.write(index, 9, amount_dict.get(s).get('kld_khaitru'), number_format)
                        sheet.write(index, 10, amount_dict.get(s).get('lld_khientrach'), number_format)
                        sheet.write(index, 11, amount_dict.get(s).get('lld_keodai'), number_format)
                        sheet.write(index, 12, amount_dict.get(s).get('lld_chuyenviec'), number_format)
                        sheet.write(index, 13, amount_dict.get(s).get('lld_khaitru'), number_format)
                        sheet.write(index, 14, amount_dict.get(s).get('lld_sathai'), number_format)
                        sheet.write(index, 15, amount_dict.get(s).get('lcb_khientrach'), number_format)
                        sheet.write(index, 16, amount_dict.get(s).get('lcb_canhcao'), number_format)
                        sheet.write(index, 17, amount_dict.get(s).get('lcb_haluong'), number_format)
                        sheet.write(index, 18, amount_dict.get(s).get('lcb_hangach'), number_format)
                        sheet.write(index, 19, amount_dict.get(s).get('lcb_cachchuc'), number_format)
                        sheet.write(index, 20, amount_dict.get(s).get('lcb_thoiviec'), number_format)
                        sheet.write(index, 21, amount_dict.get(s).get('lhs_caitao'), number_format)
                        sheet.write(index, 22, amount_dict.get(s).get('lhs_quanche'), number_format)
                        sheet.write(index, 23, amount_dict.get(s).get('lhs_tutreo'), number_format)
                        sheet.write(index, 24, amount_dict.get(s).get('lhs_tugiam'), number_format)
                        sheet.write(index, 25, amount_dict.get(s).get('lhs_tuhinh'), number_format)

                        # write next level property
                        sub_list = self.env['discipline.sub.property'].search([('level','=',line.level+1),('id','in',list_sub_pro)], order='sequence asc')

                        if len(sub_list) > 0:
                            index = index + 1
                            new_index = print_property(sub_list, index, list_tc)
                            index = new_index
                        else:
                            index = index + 1
                return index

            index = 11
            for line in list_1_level_sub_pro:
                sheet.write(index, 0, line.name, bold)

                list_tc = []
                list_tc.append(line)
                s = '|'.join(map(str, list_tc))

                if s in amount_dict.keys():
                    # write values of this row
                    discipline_reason_text = ''
                    if str(amount_dict.get(s).get('discipline_reason')) != 'False':
                        discipline_reason_text = str(amount_dict.get(s).get('discipline_reason'))
                    sheet.write(index, 1, amount_dict.get(s).get('total'), number_format)
                    sheet.write(index, 2, amount_dict.get(s).get('in_period_communist_mem'), number_format)
                    sheet.write(index, 3, amount_dict.get(s).get('in_period_women'), number_format)
                    sheet.write(index, 4, discipline_reason_text, text_wrap)
                    sheet.write(index, 5, amount_dict.get(s).get('kld_khientrach'), number_format)
                    sheet.write(index, 6, amount_dict.get(s).get('kld_canhcao'), number_format)
                    sheet.write(index, 7, amount_dict.get(s).get('kld_cachchuc'), number_format)
                    sheet.write(index, 8, amount_dict.get(s).get('kld_luudang'), number_format)
                    sheet.write(index, 9, amount_dict.get(s).get('kld_khaitru'), number_format)
                    sheet.write(index, 10, amount_dict.get(s).get('lld_khientrach'), number_format)
                    sheet.write(index, 11, amount_dict.get(s).get('lld_keodai'), number_format)
                    sheet.write(index, 12, amount_dict.get(s).get('lld_chuyenviec'), number_format)
                    sheet.write(index, 13, amount_dict.get(s).get('lld_khaitru'), number_format)
                    sheet.write(index, 14, amount_dict.get(s).get('lld_sathai'), number_format)
                    sheet.write(index, 15, amount_dict.get(s).get('lcb_khientrach'), number_format)
                    sheet.write(index, 16, amount_dict.get(s).get('lcb_canhcao'), number_format)
                    sheet.write(index, 17, amount_dict.get(s).get('lcb_haluong'), number_format)
                    sheet.write(index, 18, amount_dict.get(s).get('lcb_hangach'), number_format)
                    sheet.write(index, 19, amount_dict.get(s).get('lcb_cachchuc'), number_format)
                    sheet.write(index, 20, amount_dict.get(s).get('lcb_thoiviec'), number_format)
                    sheet.write(index, 21, amount_dict.get(s).get('lhs_caitao'), number_format)
                    sheet.write(index, 22, amount_dict.get(s).get('lhs_quanche'), number_format)
                    sheet.write(index, 23, amount_dict.get(s).get('lhs_tutreo'), number_format)
                    sheet.write(index, 24, amount_dict.get(s).get('lhs_tugiam'), number_format)
                    sheet.write(index, 25, amount_dict.get(s).get('lhs_tuhinh'), number_format)

                sub_list = self.env['discipline.sub.property'].search(
                    [('level', '=', line.level + 1), ('id', 'in', list_sub_pro)], order='sequence asc')
                list_t = []
                list_t.append(line)
                if len(sub_list) > 0:
                    index = index + 1
                    new_index = print_property(sub_list, index, list_tc)
                    index = new_index
                else:
                    index = index + 1
