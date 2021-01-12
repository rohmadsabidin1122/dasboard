# -*- coding: utf-8 -*-
##############################################################################      
#         _______  _____            _______  _       _______
#         |     | |       |       | |     | | \    |    |    |     |
#         |_____| |_____  |   _   | |_____| |  \   |    |    |_____|
#         |     |       | |  / \  | |     | |   \  |    |    |     |
#         |     |  _____| |_/   \_| |     | |    \_|    |    |     |
#                 
##############################################################################

{
    'name': 'Sale Custom Dashboard',
    'summary': 'Sale filter based sale order states',
    'author': 'Aswanth',
    'version': '12.0.1.1.0',
    'category': 'Tools',
    'depends': ['base','sale'],
    'data': [  
    	'views/sale_views.xml', 
        'views/sale_filter.xml', 
        'views/dashboard.xml',                
	],
   	'images': ['static/description/icon.png'],
   	'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}

