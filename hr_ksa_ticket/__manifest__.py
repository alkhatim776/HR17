# -*- coding: utf-8 -*-
{
    'name': "HR Ticket",

    'summary': """
        A module to manage hr employee tickets request""",

    'description': """
        Long description of module's purpose
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Human Resources',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr','hr_employee_extension','om_hr_payroll','account'],
    # 'depends': ['hr','hr_holidays','account','hr_employee_extension'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
}
