# -*- coding: utf-8 -*-
{
    'name': "Vietnamese District/Ward ",

    'summary': """
        Vietnamese District/Ward """,

    'description': """
        Thêm thông tin huyện, xã
    """,

    'author': "giangdd",
    'website': "http://gmpm.vn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/hr_ethnic_group_data.xml',
        'data/res_country_state_data.xml',
        'data/res_country_state_district_data.xml',
        'data/res_country_state_district_ward_data.xml',
        'security/security.xml',
    ],
    # only loaded in demonstration mode
    'demo': [

    ],
}
