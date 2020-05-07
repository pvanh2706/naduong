# -*- coding: utf-8 -*-
{
    'name': "MVB Document Directory",

    'summary': """
        Hỗ trợ hiển thị nhóm thư mục tài liệu văn bản theo dạng cây thư mục cho module Quản lý văn bản MVB""",

    'description': """
        Long description of module's purpose
    """,

    'author': "GMP",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mvb_documents','muk_dms', 'muk_dms_view', 'muk_dms_access'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/mvb_document_directory.xml',
        'views/document_muk_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}