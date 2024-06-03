# -*- coding: utf-8 -*-
{
    "name": "Time off extension (Saudi)",
    "summary": "Auto timeoff Allocation plus some attributes on leave type",
    "version": "16.0.0",
    'category': 'Human Resources/Leaves',
    "website": "",
    "description": """
    * Add Calculation Type [Working Days, Calendar Days] in Leave Types
    * Auto sequencing of every timeoff request
    * Auto allocation
    Define both Annual leave type and days on employee contract
    """,
    'images': [
        'static/description/cover.png'
    ],

    "author": "",
    "license": "OPL-1",
    "installable": True,
    "depends": [
        'hr_holidays', 'hr_employee_extension', 'hr_contract',
    ],
    "data": [
        'data/ir_sequence.xml',
        'data/ir_cron.xml',
        'data/hr_holidays_data.xml',
        'data/leave_plan.xml',
        'security/ir.model.access.csv',
        'view/hr_leave_type.xml',
        'view/hr_leave.xml',
        'view/hr_leave_balance.xml',
        'view/hr_contract_view.xml',
        'view/hr_employee.xml'
    ]
}
