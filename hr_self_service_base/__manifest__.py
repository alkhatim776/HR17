# -*- coding: utf-8 -*-


{
    "name": "Self Service Portal Base",
    "version": "0.1",
    "author": "Yusra Mohamed",
    "description": "",
    "depends": ['portal', 'website','web', 'hr', ],
    "external_dependencies": {"python": ["geocoder"]},
    "data" : [
        'views/assets.xml',
        'views/hr_self_service_template.xml',
        'views/portal.xml',
    ],
    # 'assets': {
    #     'web.assets_frontend': [
    #         'hr_self_service_base/static/src/js/hr_selfservice.js',
    #     ],
    # },

    'qweb': [],
    'installable': True,
    'application': True,
}
