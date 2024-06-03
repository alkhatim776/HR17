# -*- coding: utf-8 -*-
{
    'name': "HR Attendance Extension (Saudi)",

    'summary': """hr attendance base customization""",

    'description': """
        hr attendance base customization
    """,

    'author': "",
    'category': 'Human Resources/Attendance',
    'version': '16.0',

    'depends': ['hr_contract','hr_attendance', 'hr_payroll_extension','hr_employee_extension'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/payroll_data.xml',
        'data/salary_rules.xml',
        'data/hr_payroll_structure_data.xml',
        'views/hr_contract.xml',
        'views/hr_attendance.xml',
        'views/attendance_deduction_view.xml',
        'views/hr_sheet_print.xml',
        'views/hr_attendance_rules.xml'
    ],
    
}
