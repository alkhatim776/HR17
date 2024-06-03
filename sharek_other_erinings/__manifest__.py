# -*- coding: utf-8 -*-
{
    'name': "Employee Other Earnings",
    'summary': "Any kind of deduction or fine or allowance in form of money can given to employees based on different filter like department, project, job position or all",
    'description': "Employee Other Earnings",
    'category': 'Generic Modules/Human Resources',
    'version': '15.0.0',
    'author':'',
    'website': "",
    'depends': ['project', 'hr_work_entry_contract', 'account', 'hr_timesheet'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/other_earnings.xml',
        'views/res_config_settings_view.xml'
    ],
    'installable': True,
    'application': True,
}
