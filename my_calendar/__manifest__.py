# -*- coding: utf-8 -*-
{
    'name': "Lịch công tác",

    'summary': """
      Đây là lịch công tác của các lãnh đạo""",

    'description': """
        Quản lý lịnh công tác của các lãnh đạo
    """,

    'author': "Đổi mới Group",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'portal'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/group_security.xml',
        'wizards/doimoi_total_calendar.xml',
        'wizards/content_calendar_edit.xml',
        'wizards/document_guide.xml',
        'views/calendar_views.xml',
        'views/total_calendar_views.xml',
        'views/templates.xml',
        # 'data/channel_calendar_messenger.xml',
        'reports/calendar_pdf.xml',
        'reports/report.xml',
        'views/menu.xml',
    ],
    'qweb': ['static/src/xml/doimoi_tree_view_button.xml'],

}
