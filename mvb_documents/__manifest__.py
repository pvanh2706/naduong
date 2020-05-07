# -*- coding: utf-8 -*-
{
    'name': "MVB Documents",

    'summary': """
        Module quản lý các tài liệu của công ty
        """,

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'mail','mvb_company','report_xlsx'],

    # always loaded
    'data': [
        'security/security_data.xml',
        'security/mvb_rule.xml',
        'security/ir.model.access.csv',

        'data/document_type_data.xml',
        'data/mvb_cron_document.xml',
        'data/mail_template_data.xml',

        'views/mvb_document_views.xml',
        'views/mvb_document_type.xml',
        'views/mvb_document_contract_type.xml',
        'views/mvb_document_groups.xml',
        'views/mvb_document_action.xml',
        'views/document_publisher_views.xml',
        'views/mvb_document_notebook.xml',
        'views/mvb_document_menu.xml',
        'views/mvb_project_view.xml',
        'views/mvb_project_bidding_package_view.xml',
        'views/mvb_project_phase_view.xml',
        'views/mvb_document_guide.xml',

        'report/report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}