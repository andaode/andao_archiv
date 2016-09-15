# -*- coding: utf-8 -*-
{
    'name': "Archive",

    'summary': """
        A module for archiving data""",

    'description': """
        This module reads the files
    """,

    'author': "Andrzej Gr",
    'website': "http://www.andao.de/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Archive',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ["mail"],

    # always loaded
    'data': [

         'views/menu.xml',
         'views/main_view.xml',
         'views/contact.xml',
         'security/security_groups_and_rules.xml',
         'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo.xml',
    ],

}
