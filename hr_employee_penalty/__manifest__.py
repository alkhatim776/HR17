# -*- coding: utf-8 -*-
{
    'name': "HR Employee Penalty (Saudi)",

    'summary': """
        A module to manage hr employee penalties""",

    'description': """
        Long description of module's purpose
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Human Resources',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr','hr_payroll_extension','hr_employee_extension','mail','om_account_accountant','om_hr_payroll'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/hr_employee_inherit.xml',
        'views/hr_salary_rule_view.xml',
        'data/penalty_data.xml',
    ],
}
