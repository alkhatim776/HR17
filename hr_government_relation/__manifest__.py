# -*- coding: utf-8 -*-
{
    'name': "HR Government Relation",

    'summary': """
        A module to manage governments procedure""",

    'description': """
        Long description of module's purpose
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Human Resources',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['hr_contract', 'hr_employee_extension', 'hr_holidays', 'account', 'mail', 'hr_employee_family',
                'om_hr_payroll'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings.xml',
        'views/exit_return.xml',
        'views/iqama_renewal.xml',
    ],
}
