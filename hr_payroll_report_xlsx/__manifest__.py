# -*- coding: utf-8 -*-
{
    'name': "Hr Payroll Report Xlsx",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Yusra mohamed",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    "category": "Human Resources/Payroll",
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','om_hr_payroll','report_xlsx'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        
    ],
    # only loaded in demonstration mode
    "installable": True,
}
