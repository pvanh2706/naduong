# -*- coding: utf-8 -*-
{
    'name': "HR Company of MVB",

    'summary': """
        HR Company of MVB""",

    'description': """
        HR Company of MVB
    """,

    'author': "gmpm",

    'category': 'HR',
    'version': '12',

    'depends': ['base','hr_recruitment'],


    'data': [
         'views/hr_company_views.xml',
         'views/hr_department_views.xml',
         'data/company_data.xml',
         'data/department_data.xml',
         'views/hr_job_views.xml',
        # 'security/ir.model.access.csv',
        # 'report/report.xml',
    ],
}
