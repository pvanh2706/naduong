# -*- coding: utf-8 -*-
{
    'name': "G_mail",

    'summary': """
        Module quản lý thư đi đến của hệ thống""",
    'description': """
       Phần mền giúp quản lý Gmail đến và đi
    """,

    'author': "Đổi mới Group",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/g_mail_group.xml',
        'security/ir.model.access.csv',
        'wizards/extend_mail_compose_message.xml',
        'views/mail_box_views.xml',
        'views/sent_mail_box.xml',
        'views/mail_menu.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
