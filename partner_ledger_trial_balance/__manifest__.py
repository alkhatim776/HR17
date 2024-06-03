# -*- coding: utf-8 -*-

{
    'name': 'Partner Ledger Trail Balance',

    'summary': """Partner Ledger Trail Balance""",

    'description': """ Partner Ledger Trail Balance""",

    'author': "Business Horizons",
    'website': "",
    'license': 'LGPL-3',
    'version': '17.1',
    'category': 'Accounting/Accounting',
    'depends': ['account_reports', 'report_xlsx'],

    'data': [
        'security/ir.model.access.csv',
        'reports/report_partnerledger.xml',
        'reports/report.xml',
        'wizard/partner_ledger_wiz_views.xml',
    ],
    
    


    'installable': True,
    'auto_install': False,
}
