# -*- coding: utf-8 -*-
{
    'name': "Quản lý nhân sự",

    'summary': """
        Quản lý nhân sự""",

    'description': """
        Quản lý nhân sự
    """,

    'author': "gmpm",

    'category': 'Nhân sự',
    'version': '12',

    'depends': ['base', 'l11n_vn_country_state', 'hr','hr_contract','hr_payroll' ,'report_xlsx'],


    'data': [
        'security/security_data.xml',

        'wizard/hr_employee_code_edit.xml',
        'wizard/payroll_report_gen_property_views.xml',
        'wizard/training_report_gen_property_views.xml',
        'views/hr_contract_views.xml',
        'views/hr_document_views.xml',
        'views/hr_employee_views.xml',
        'views/hr_instruction_views.xml',
        'views/hr_work_process.xml',
        'views/study_process_views.xml',
        'views/extend_res_users.xml',
        # 'views/hr_employee_report_views.xml',
        'security/ir.model.access.csv',
        'report/report.xml',
        # 'views/hr_current_address.xml',
        # 'views/payroll_property_list_views.xml',
        # 'views/payroll_year_plan_views.xml',
        # 'views/payroll_year_report_views.xml',
        # 'views/training_property_list_views.xml',
        # 'views/training_plan_views.xml',
        # 'views/training_report_views.xml',
        # 'views/discipline_report_views.xml',
        # 'views/discipline_property_views.xml',

        # 'data/hr_ethnic_group_data.xml',
        # 'data/payroll_property.xml',
        # 'data/training_property.xml',
        # 'data/training_report_data.xml',
        # 'data/discipline_property.xml',
        # 'data/discipline_report_data.xml',
        # 'data/hr_bonus_type_data.xml',
    ],
}
