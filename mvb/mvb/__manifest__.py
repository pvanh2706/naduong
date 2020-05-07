# -*- coding: utf-8 -*-
{
    'name': "MVB",

    'summary': """
        MVB""",

    'description': """
        HR Company of MVB
    """,

    'author': "gmpm",

    'category': 'HR',
    'version': '12',

    'depends': ['mvb_hr',
                'mvb_company',
                'mvb_documents',
                'mvb_document_directory',
                'mvb_eoffice',
                ],

    'data': [
        'security/ir.model.access.csv',
        'security/security_group.xml',

        # 'data/security_rule.xml',
        'views/recruitment_views.xml',
        'views/notification.xml',
        'views/contact_views.xml',
        'views/calendar_views.xml',
        'views/holidays_views.xml',
        'views/mail_views.xml',
        'views/hide_menu_hr.xml',
        # 'views/department_views.xml',
        # 'views/hr_education_views.xml',
        'views/payroll_views.xml',
        'views/muk_document_views.xml',
        # 'views/hr_menu_views.xml',
        # 'views/custom_menu.xml',
    ],
}
