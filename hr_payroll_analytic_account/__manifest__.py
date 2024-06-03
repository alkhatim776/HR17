# -*- coding: utf-8 -*-

{
    'name': "HR Payroll Analytic account",
    'summary': """Create entry from HR with analytic account in specific types of account""",
    'description': """
    """,
    'author': 'Business Horizone',
    'category': 'Human Resources',
    'version': '16.0',
    'depends': ['om_hr_payroll'],
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        # 'security/security.xml',
        'views/res_config_settings_view.xml',
    ],
}
