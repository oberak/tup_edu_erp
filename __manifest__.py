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
    'depends': ['base', 'auth_signup', 'hr_recruitment', 'education_core', 'education_time_table', 'education_promotion', 'education_fee'],

    # always loaded
    'data': [
        ## security
        'security/education_core/education_security.xml',
        'security/education_core/ir.model.access.csv',
        'security/education_exam/ir.model.access.csv',
        'security/education_fee/ir.model.access.csv',
        'security/education_promotion/ir.model.access.csv',
        'security/ir.model.access.csv',

        ## data
        'data/auth_sighup_data.xml',
        'data/education_data.xml',
        'data/timetable_period_data.xml',

        ## template
        'views/auth_signup/auth_oauth_templates.xml',

        ## view - attendance
        'views/attendance/students_attendance.xml',

        ## view - hr_recruitment
        'views/hr_recruitment/hr_department.xml',
        'views/hr_recruitment/hr_employee.xml',

        ## view - education_core
        'views/education_core/education_application.xml',
        'views/education_core/education_class_division.xml',
        'views/education_core/education_class.xml',
        'views/education_core/education_division.xml',
        'views/education_core/education_faculty.xml',
        'views/education_core/education_student_class.xml',
        'views/education_core/education_subject.xml',
        'views/education_core/education_syllabus.xml',

        ## view - education_time_table
        'views/education_time_table/education_time_table.xml',
        'views/education_time_table/timetable_schedule.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}