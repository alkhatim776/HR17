# -*- coding: utf-8 -*-

{
    "name": "Employee Additional Information",
    "summary": "Employee Additional Information(Saudi)",
    'category': 'Human Resources',
    "description": """
        Additional Information.
         
    """,
    
    "author": "",
    "license": "OPL-1",
    'website': "",
    "version": "17.0",
    "installable": True,
    "depends": [
        'hr','hr_contract','hr_payroll_extension','om_hr_payroll'
    ],
    "data": [
        'security/ir.model.access.csv',
        'view/hr_employee.xml',
        'view/res_config_settings.xml',
        'data/data.xml',
        'report/employee_details_report.xml',
    ],
    'images': [
        
    ],
    # 'odoo-apps' : True
}

