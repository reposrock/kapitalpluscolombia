# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name" : "Purchase Budget Limit Warning/Alerts - Enterprise",
    "version" : "14.0.0.2",
    "category" : "Accounting",
    'summary': "Integrate budget with purchase Analytic account restrict override budget amount purchase Accounting budget purchase integration with budget purchase budget alerts budget vendor bill costing purchase budget costing budget warning budget restriction alerts",
    "description": """
    
    Purchase Order Integration with Budget in Odoo(Enterprise Edition),
    Purchese order budget intigration in odoo,
    Purchese order intigration with budget app in odoo,
    Purchese order budget intigration odoo app,
    override Purchese order budget amount in odoo,
    allow override Purchese order budget amount in odoo,
    resterict override Purchese order budget amount in odoo,

    """,
    "author": "BrowseInfo",
    "website" : "https://www.browseinfo.in",
    "price": 49,
    "currency": 'EUR',
    "depends" : ['base','account_budget','purchase','account'],
    "data": ['views/purchase.xml',
             'views/account_budget_views.xml',
             'views/res_config_settings_views.xml',
             ],
    'demo': [],
    'qweb': [],
    "auto_install": False,
    "installable": True,
    "live_test_url":'https://youtu.be/ST689Frn7CQ',
    "images":["static/description/Banner.png"],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
