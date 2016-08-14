# -*- coding: utf-8 -*-
{
    'name': "OCR",

    'summary': """
        A module for reading text from jpg""",

    'description': """
        This module reads and work with invoices
    """,

    'author': "Grand City Property Ltd.",
    'website': "http://www.grandcityproperties.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ["mail"],

    # always loaded
    'data': [
       # 'security/ir.model.access.csv',
         'views/menu.xml',
         'views/main_view.xml',
         'views/contact.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo.xml',
    ],

}
