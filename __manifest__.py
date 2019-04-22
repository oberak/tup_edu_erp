# -*- coding: utf-8 -*-
{
    'name': "Educational ERP for TUP",

    'summary': """
        Education ERP extension module for Technological University( Pathein )
        """,

    'description': """
        Education ERP extension module for Technological University( Pathein )
    """,

    'author': "Technological University( Pathein )",
    'website': "http://tup.edu.mm",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Employees',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'auth_signup', 'education_core'],

    # always loaded
    'data': [
        ## security
        'security/education_core/education_security.xml',
        'security/education_core/ir.model.access.csv',
        'security/ir.model.access.csv',

        ## data
        'data/auth_sighup_data.xml',
        'data/education_data.xml',

        ## template
        'views/tup_auth_oauth_templates.xml',

        ## view - hr
        'views/tup_hr_department.xml',

        ## view - education_core
        'views/tup_education_application.xml',
        'views/tup_education_faculty.xml',
        'views/tup_education_time_table.xml',
        'views/tup_education_subject.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}