from odoo import models
from datetime import datetime, date

class ReportTrainingXlsx(models.AbstractModel):
    _name = 'report.mvb_hr.training_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        for obj in objs:

            sheet = workbook.add_worksheet('Năm '+str(obj.plan_id.year))
            bold = workbook.add_format({'bold': True, 'border':True})
            text_wrap = workbook.add_format({
                'text_wrap': True,
                'align': 'center',
                'valign': 'vcenter',
                'border':True
            })
            property_1 = workbook.add_format({
                'bold': True,
                'border':True
            })
            number_format = workbook.add_format({
                'num_format': '###,###,###','border':True
            })
            border = workbook.add_format({'border': True})
            center = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'border':True})
            header_title = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'font_size': 12,
                'text_wrap': True,
            })
            header_main_title = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'bold': True,
                'font_size': 12,
                'text_wrap': True,
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
                'text_wrap': True,
                'border':True,
                'bold': True,
            })

            text_normal = workbook.add_format({
                'text_wrap': True,
                'align': 'right',
            })

            text_no_border = workbook.add_format({
                'text_wrap': True,
                'align': 'center',
            }) 

            sheet.merge_range("A1:C1", "TẬP ĐOÀN CÔNG NGHIỆP", header_main_title)
            sheet.merge_range("A2:C2", "THAN KHOÁNG SẢN VIỆT NAM", header_main_title)
            sheet.merge_range("A3:C3", "TÊN ĐƠN VỊ", header_main_title)
            sheet.merge_range("A4:N4", "BÁO CÁO THỰC HIỆN CÔNG TÁC ĐÀO TẠO, BỒI DƯỠNG " + str(
                obj.plan_id.year), header_main_title)
            sheet.merge_range("A5:N5", "(Áp dụng cho các đơn vị thuộc VINACOMIN)", text_no_border)

            sheet.merge_range("L1:N1", "Biểu 19/ĐLTL", text_normal)
            sheet.merge_range("L2:N2", "Ngày nhận 05/01 hàng năm", text_normal)
            sheet.merge_range("L3:N3", "Nơi nhận: Ban LĐTL", text_normal)

            # set col size
            sheet.set_column('A:A', 3, border)
            sheet.set_column('B:B', 50, border)
            sheet.set_column('C:N', 13)

            # write header
            sheet.merge_range("A6:A8", "STT", header)
            sheet.merge_range("B6:B8", "Nội dung đào tạo, bồi dưỡng", header)
            sheet.merge_range("C6:I6", "Thực hiện năm "+ str(obj.plan_id.year), header)
            sheet.merge_range("J6:N6", "Kế hoạch năm tiếp theo",header)
            sheet.merge_range("C7:E7", "Số người",header)
            sheet.merge_range("F7:I7", "Kinh phí (Triệu đồng)",header)
            sheet.merge_range("J7:J8", "Số người dự học",header)
            sheet.merge_range("K7:N7", "Kinh phí (Triệu đồng)",header)
            sheet.write("C8", "Dự học",text_wrap)
            sheet.write("D8", "Đạt yêu cầu",text_wrap)
            sheet.write("E8", "Tỷ lệ (%)",text_wrap)
            sheet.write("F8", "Công ty",text_wrap)
            sheet.write("G8", "Tập đoàn",text_wrap)
            sheet.write("H8", "Khác",text_wrap)
            sheet.write("I8", "Tổng số",text_wrap)
            sheet.write("K8", "Công ty",text_wrap)
            sheet.write("L8", "Tập đoàn",text_wrap)
            sheet.write("M8", "Khác",text_wrap)
            sheet.write("N8", "Tổng số",text_wrap)

            sheet.write("A9", "A",text_wrap)
            sheet.write("B9", "B",text_wrap)
            sheet.write("C9", "(1)",text_wrap)
            sheet.write("D9", "(2)",text_wrap)
            sheet.write("E9", "(3)=(2)(1)x100%",text_wrap)
            sheet.write("F9", "(4)",text_wrap)
            sheet.write("G9", "(5)",text_wrap)
            sheet.write("H9", "(6)",text_wrap)
            sheet.write("I9", "(7)=(4)+(5)+(6)",text_wrap)
            sheet.write("J9", "(8)",text_wrap)
            sheet.write("K9", "(9)",text_wrap)
            sheet.write("L9", "(10)",text_wrap)
            sheet.write("M9", "(11)",text_wrap)
            sheet.write("N9", "(12)=(9)+(10)+(11)",text_wrap)
            
            sheet.write("B10","TỔNG SỐ (I + II)",text_wrap)
            sheet.write("C10", "=SUM(C11,C44)",number_format)
            sheet.write("D10", "=SUM(D11,D44)",number_format)
            sheet.write("E10", "=SUM(E11,E44)",number_format)
            sheet.write("F10", "=SUM(F11,F44)",number_format)
            sheet.write("G10", "=SUM(G11,G44)",number_format)
            sheet.write("H10", "=SUM(H11,H44)",number_format)
            sheet.write("I10", "=SUM(I11,I44)",number_format)
            sheet.write("J10", "=SUM(J11,J44)",number_format)
            sheet.write("K10", "=SUM(K11,K44)",number_format)
            sheet.write("L10", "=SUM(L11,L44)",number_format)
            sheet.write("M10", "=SUM(M11,M44)",number_format)
            sheet.write("N10", "=SUM(K10,L10,M10)",number_format)

            sheet.freeze_panes('A10:N10')

            list_sub_pro = []
            list_1_level_sub_pro = []
            amount_dict = dict()
            amount_plan_total = dict()

            # get value from report
            for line in obj.line_ids:
                list_sub_t = []
                for li in line.property_id.property_ids:
                    list_sub_t.append(li)
                    s = '|'.join(map(str, list_sub_t))
                    if s not in amount_dict.keys():
                        new_dict = dict()
                        new_dict['attendees_amount'] = line.attendees_amount
                        new_dict['qualified'] = line.qualified
                        new_dict['percent'] = line.percent
                        new_dict['company_amount'] = line.company_amount
                        new_dict['group_amount'] = line.group_amount
                        new_dict['other_amount'] = line.other_amount
                        new_dict['total_amount'] = line.total_amount
                        amount_dict [s] = new_dict
                    else:
                        amount_dict.get(s)['attendees_amount'] = amount_dict.get(s)['attendees_amount'] + line.attendees_amount
                        amount_dict.get(s)['qualified'] = amount_dict.get(s)['qualified'] + line.qualified
                        amount_dict.get(s)['percent'] = amount_dict.get(s)['percent'] + line.percent
                        amount_dict.get(s)['company_amount'] = amount_dict.get(s)['company_amount'] + line.company_amount
                        amount_dict.get(s)['group_amount'] = amount_dict.get(s)['group_amount'] + line.group_amount
                        amount_dict.get(s)['other_amount'] = amount_dict.get(s)['other_amount'] + line.other_amount
                        amount_dict.get(s)['total_amount'] = amount_dict.get(s)['total_amount'] + line.total_amount

                    if li.id not in list_sub_pro:
                        list_sub_pro.append(li.id)
                    if li not in list_1_level_sub_pro and li.level == 1:
                        list_1_level_sub_pro.append(li)

            # get value from plan
            for line in obj.plan_id.line_ids:
                list_sub_t = []
                for li in line.property_id.property_ids:
                    if li.id not in list_sub_pro:
                        list_sub_pro.append(li.id)
                    if li not in list_1_level_sub_pro and li.level == 1:
                        list_1_level_sub_pro.append(li)
                    list_sub_t.append(li)

                    s = '|'.join(map(str, list_sub_t))

                    if s not in amount_plan_total.keys():
                        new_dict = dict()
                        new_dict['attendees_expected_amount'] = line.attendees_expected_amount
                        new_dict['company_expected_amount'] = line.company_expected_amount
                        new_dict['group_expected_amount'] = line.group_expected_amount
                        new_dict['other_expected_amount'] = line.other_expected_amount
                        new_dict['total_expected_amount'] = line.total_expected_amount
                        
                        amount_plan_total[s] = new_dict
                        if s not in amount_dict.keys():
                            new_dict = dict()
                            amount_dict[s] = new_dict
                    else:
                        amount_plan_total.get(s)['attendees_expected_amount'] = amount_plan_total.get(s)['attendees_expected_amount'] + line.attendees_expected_amount
                        amount_plan_total.get(s)['company_expected_amount'] = amount_plan_total.get(s)['company_expected_amount'] + line.company_expected_amount
                        amount_plan_total.get(s)['group_expected_amount'] = amount_plan_total.get(s)['group_expected_amount'] + line.group_expected_amount
                        amount_plan_total.get(s)['other_expected_amount'] = amount_plan_total.get(s)['other_expected_amount'] + line.other_expected_amount
                        amount_plan_total.get(s)['total_expected_amount'] = amount_plan_total.get(s)['total_expected_amount'] + line.total_expected_amount

            def sortSecond(val):
                return val.sequence
            list_1_level_sub_pro.sort(key = sortSecond)

            def print_property(list, index, list_t):
                i=0
                j=0
                k=0
                first = True
                for line in list:

                    list_tc = list_t.copy()
                    list_tc.append(line)
                    s = '|'.join(map(str, list_tc))

                    if s in amount_dict.keys():
                        # in stt va ten tieu chi
                        if(len(s.split('|')) == 2):
                            sheet.write(index, 1, line.name, bold)
                            sheet.write(index, 0,stt_lv2[i], stt_bold)

                        elif(len(s.split('|')) == 3):
                            sheet.write(index, 1, line.name, bold)
                            sheet.write(index, 0, stt_lv3[i], stt_bold)
                            stt_current_3.append(stt_lv3[i])

                        elif(len(s.split('|')) == 4):
                            sheet.write(index, 1, line.name, border)
                            if first == True:
                                k = j - 1
                                first = False
                            sheet.write(index,0, str(stt_current_3[k]) + '.' + str(stt_lv4[j]), stt)                            
                            j = j + 1
                        else:
                            sheet.write(index, 1, line.name,border)
                        i = i + 1

                        # write values of this row
                        sheet.write(index, 2, amount_dict.get(s).get('attendees_amount'), number_format)
                        sheet.write(index, 3, amount_dict.get(s).get('qualified'), number_format)
                        sheet.write(index, 4, amount_dict.get(s).get('percent'), number_format)
                        sheet.write(index, 5, amount_dict.get(s).get('company_amount'), number_format)
                        sheet.write(index, 6, amount_dict.get(s).get('group_amount'), number_format)
                        sheet.write(index, 7, amount_dict.get(s).get('other_amount'), number_format)
                        sheet.write(index, 8, amount_dict.get(s).get('total_amount'), number_format)

                    if s in amount_plan_total.keys():
                        sheet.write(index, 9, amount_plan_total.get(s).get('attendees_expected_amount'), number_format)
                        sheet.write(index, 10, amount_plan_total.get(s).get('company_expected_amount'), number_format)
                        sheet.write(index, 11, amount_plan_total.get(s).get('group_expected_amount'), number_format)
                        sheet.write(index, 12, amount_plan_total.get(s).get('other_expected_amount'), number_format)
                        sheet.write(index, 13, amount_plan_total.get(s).get('total_expected_amount'), number_format)
                        
                        # write next level property
                        sub_list = self.env['train.plan.sub.property'].search([('level','=',line.level+1),('id','in',list_sub_pro)], order='sequence asc')

                        if len(sub_list) > 0:
                            index = index + 1
                            new_index = print_property(sub_list, index, list_tc)
                            index = new_index
                        else:
                            index = index + 1
                return index
            stt_lv1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
            stt_lv2 = ['I','II','III','IV','V','VI','VII','VIII','IX','X']
            stt_lv3 = range(1,30)
            stt_lv4 = range(1,30)
            stt_current_3 = []
            e=0
            index = 10
            for line in list_1_level_sub_pro:
                sheet.write(index, 1, line.name, bold)
                sheet.write(index, 0, stt_lv1[e], stt_bold)
                e = e + 1

                list_tc = []
                list_tc.append(line)
                s = '|'.join(map(str, list_tc))

                if s in amount_dict.keys():
                    # write values of this row
                    sheet.write(index, 2, amount_dict.get(s).get('attendees_amount'), number_format)
                    sheet.write(index, 3, amount_dict.get(s).get('qualified'), number_format)
                    sheet.write(index, 4, amount_dict.get(s).get('percent'), number_format)
                    sheet.write(index, 5, amount_dict.get(s).get('company_amount'), number_format)
                    sheet.write(index, 6, amount_dict.get(s).get('group_amount'), number_format)
                    sheet.write(index, 7, amount_dict.get(s).get('other_amount'), number_format)
                    sheet.write(index, 8, amount_dict.get(s).get('total_amount'), number_format)

                if s in amount_plan_total.keys():
                    sheet.write(index, 9, amount_plan_total.get(s).get('attendees_expected_amount'), number_format)
                    sheet.write(index, 10, amount_plan_total.get(s).get('company_expected_amount'), number_format)
                    sheet.write(index, 11, amount_plan_total.get(s).get('group_expected_amount'), number_format)
                    sheet.write(index, 12, amount_plan_total.get(s).get('other_expected_amount'), number_format)
                    sheet.write(index, 13, amount_plan_total.get(s).get('total_expected_amount'), number_format)

                sub_list = self.env['train.plan.sub.property'].search(
                    [('level', '=', line.level + 1), ('id', 'in', list_sub_pro)], order='sequence asc')
                list_t = []
                list_t.append(line)
                if len(sub_list) > 0:
                    index = index + 1
                    new_index = print_property(sub_list, index, list_tc)
                    index = new_index
                else:
                    index = index + 1