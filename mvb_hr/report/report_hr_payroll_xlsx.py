from odoo import models
from datetime import datetime, date

class ReportHrPayrollXlsx(models.AbstractModel):
    _name = 'report.mvb_hr.payroll_report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        for obj in objs:

            sheet = workbook.add_worksheet('TH '+ str(obj.month) + '-'+str(obj.plan_id.year))
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
                'font_size': 10,
                'text_wrap': True,
                'border':True
            })
            header_main_title = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'bold': True,
                'font_size': 12,
                'text_wrap': True,
                'border':True
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
                'border':True
            })

            # set title
            sheet.merge_range('A1:B1','TẬP ĐOÀN CÔNG NGHIỆP THAN - KHOÁNG SẢN VIỆT NAM',header_main_title)
            sheet.merge_range('A2:B2','ĐƠN VỊ',header_main_title)
            sheet.merge_range("A3:G3", "BÁO CÁO NHANH LAO ĐỘNG TIỀN LƯƠNG THÁNG " + str(obj.month) + ' NĂM ' + str(
                obj.plan_id.year), header_main_title)
            sheet.merge_range('F1:G1','Mẫu BCN/LDTL-TKV',text_wrap)
            sheet.merge_range('F2:G2','Ngày nhận: 20 tháng BC',text_wrap)
            # set col size
            sheet.set_column('A:A', 8, border)
            sheet.set_column('B:B', 40, border)
            sheet.set_column('C:G', 15, border)
            



            # write header
            sheet.write("A4", "STT", header)
            sheet.write("B4", "CHỈ TIÊU",header)
            sheet.write("C4", "ĐƠN VỊ TÍNH",header)
            sheet.write("D4", "KH NĂM",header)
            sheet.write("E4", "THỰC HIỆN THÁNG TRƯỚC",header)
            sheet.write("F4", "ƯỚC TÍNH THÁNG BÁO CÁO",header)
            sheet.write("G4", "CỘNG DỒN NĂM",header)

            # processing data
            list_sub_pro = []
            list_1_level_sub_pro = []
            amount_dict = dict()
            plan_amount_dict = dict()

            # get value from report
            for line in obj.line_ids:
                list_sub_t = []
                for li in line.property_id.property_ids:
                    list_sub_t.append(li)
                    s = '|'.join(map(str, list_sub_t))
                    if s not in amount_dict.keys():
                        new_dict = dict()
                        new_dict['unit'] = line.property_id.unit
                        new_dict['amount'] = line.amount
                        new_dict['estimated_report_month'] = line.estimated_report_month
                        new_dict['cumulative_year'] = line.cumulative_year

                        amount_dict [s] = new_dict
                    else:
                        amount_dict.get(s)['amount'] = amount_dict.get(s)['amount'] + line.amount
                        amount_dict.get(s)['estimated_report_month'] = amount_dict.get(s)[
                                                                           'estimated_report_month'] + line.estimated_report_month
                        amount_dict.get(s)['cumulative_year'] = amount_dict.get(s)[
                                                                    'cumulative_year'] + line.cumulative_year

                    if li.id not in list_sub_pro:
                        list_sub_pro.append(li.id)
                    if li not in list_1_level_sub_pro and li.level == 1:
                        list_1_level_sub_pro.append(li)

            for line in obj.plan_id.line_ids:
                list_sub_t = []
                for li in line.property_id.property_ids:
                    list_sub_t.append(li)

                    s = '|'.join(map(str, list_sub_t))
                    if s not in plan_amount_dict.keys():
                        new_dict = dict()
                        new_dict['expected_year_amount'] = line.expected_year_amount

                        plan_amount_dict[s] = new_dict
                    else:
                        plan_amount_dict.get(s)['expected_year_amount'] = plan_amount_dict.get(s)[
                                                                              'expected_year_amount'] + line.expected_year_amount

                    if s not in amount_dict.keys():
                        new_dict = dict()
                        amount_dict[s] = new_dict

                    if li.id not in list_sub_pro:
                        list_sub_pro.append(li.id)
                    if li not in list_1_level_sub_pro and li.level == 1:
                        list_1_level_sub_pro.append(li)

            print (amount_dict)
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
                            sheet.write(index, 1, line.name, border)
                            sheet.write(index, 0, stt_lv3[i], stt)
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
                        if amount_dict.get(s).get('unit'):
                            sheet.write(index, 2, amount_dict.get(s).get('unit'), number_format)
                        if s in plan_amount_dict.keys():
                            sheet.write(index, 3, plan_amount_dict.get(s).get('expected_year_amount'), number_format)
                        sheet.write(index, 4, amount_dict.get(s).get('amount'), number_format)
                        sheet.write(index, 5, amount_dict.get(s).get('estimated_report_month'), number_format)
                        sheet.write(index, 6, amount_dict.get(s).get('cumulative_year'), number_format)

                        # write next level property
                        sub_list = self.env['payroll.plan.sub.property'].search(
                            [('level', '=', line.level + 1), ('id', 'in', list_sub_pro)], order='sequence asc')

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

            index = 4
            for line in list_1_level_sub_pro:
                sheet.write(index, 1, line.name, property_1)
                sheet.write(index, 0, stt_lv1[e], stt_bold)
                e = e + 1

                s = str(line)
                # write values of this row
                if s in amount_dict.keys():
                    if amount_dict.get(s).get('unit'):
                        sheet.write(index, 2, amount_dict.get(s).get('unit'), number_format)
                    if s in plan_amount_dict.keys():
                        sheet.write(index, 3, plan_amount_dict.get(s).get('expected_year_amount'), number_format)
                    sheet.write(index, 4, amount_dict.get(s).get('amount'), number_format)
                    sheet.write(index, 5, amount_dict.get(s).get('estimated_report_month'), number_format)
                    sheet.write(index, 6, amount_dict.get(s).get('cumulative_year'), number_format)

                sub_list = self.env['payroll.plan.sub.property'].search(
                    [('level', '=', line.level + 1), ('id', 'in', list_sub_pro)], order='sequence asc')
                list_t = []
                list_t.append(line)
                if len(sub_list) > 0:
                    index = index + 1
                    new_index = print_property(sub_list, index, list_t)
                    index = new_index
                else:
                    index = index + 1

            sheet.write_formula('D20', '=D14+D16-D18', number_format)
            sheet.write_formula('E20', '=E14+E16-E18', number_format)
            sheet.write_formula('F20', '=F14+F16-F18', number_format)
            sheet.write_formula('G20', '=G14+G16-G18', number_format)

            sheet.write_formula('D30', '=IF(D27=0, 0, D8/D27/12)', number_format)
            sheet.write_formula('E30', '=IF(E27=0, 0, E8/E27)', number_format)
            sheet.write_formula('F30', '=IF(F27=0, 0, F8/F27)', number_format)
            sheet.write_formula('G30', '=IF(G27=0, 0, G8/G27/H1)', number_format)

            sheet.write('H1', str(int(obj.month)-1), number_format)

            sheet.write_formula('D31', '=IF(D28>0,D9/D28/12,0)', number_format)
            sheet.write_formula('E31', '=IF(E28>0,E9/E28,0)', number_format)
            sheet.write_formula('F31', '=IF(F28>0,F9/F28,0)', number_format)
            sheet.write_formula('G31', '=IF(G28>0,G9/G28/H1,0)', number_format)

            sheet.write_formula('D32', '=IF(D27=0,0,D12/D27/12)', number_format)
            sheet.write_formula('E32', '=IF(E27=0,0,E12/E27)', number_format)
            sheet.write_formula('F32', '=IF(F27=0,0,F12/F27)', number_format)
            sheet.write_formula('G32', '=IF(G27=0,0,G12/G27/H1)', number_format)
