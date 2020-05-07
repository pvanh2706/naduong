# -*- coding: utf-8 -*-
{
    'name': "Quản lý VB và điều hành",

    'summary': """
        Module quản lý văn bản điện tử cho công ty""",

    'description': """
        Văn phòng điện tử
    """,

    'author': "gmpm",

    'category': 'HR',
    'version': '12',

    'depends': ['base', 'mvb_documents', 'my_calendar'],

    'data': [
        'data/sequence.xml',
        'data/cron.xml',
        'security/mvb_eoffice_rule.xml',
        'security/security_data.xml',
        'security/ir.model.access.csv',
        'wizards/mvb_text_direction_wizard_view.xml',
        'wizards/mvb_text_draft_wizard.xml',
        'wizards/mvb_range_date.xml',
        'wizards/dash_board_action.xml',
        # 'views/mvb_dashboard.xml',
        'views/mvb_waiting_solution.xml',
        'views/mvb_calendar_work_views.xml',
        'views/mvb_incoming_text.xml',
        'views/mvb_text_go.xml',
        'views/mvb_draft_text_go_views.xml',
        'views/mvb_text_action.xml',
        'views/mvb_text_process_view.xml',
        'views/mvb_templates.xml',
        'views/job_profile_views.xml',
        'views/mvb_processing_textdraft.xml',
        # 'views/dashboard_eoffice.xml',
        'reports/document_go_pdf.xml',
        'reports/report.xml',
        'views/mvb_text_menu.xml',

    ],
    'qweb': ["static/src/xml/doc_dash_board.xml",
            # "static/src/xml/user_menu.xml",
            ],
}
