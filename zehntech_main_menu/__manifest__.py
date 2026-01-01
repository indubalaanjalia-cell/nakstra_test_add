{
    'name': 'Main Menu',
     "version": "17.0.1.0.0",
    'category': 'Technical/Technical',
    'sequence': 1,
    'summary': """The Main Menu module for Odoo Community Edition provides a streamlined dashboard for seamless navigation across core modules.
                  Featuring dynamic widgets for real-time date display and administrator-managed announcements, it enhances user efficiency.
                  Custom bookmarking allows users to organize essential menus and external links, improving workflow and accessibility within
                  the Odoo backend.""",
    'description': 'Enhance navigation and workflow efficiency with the Main Menu module for Odoo Community Edition. This module introduces a centralized dashboard, enabling quick access to core modules and frequently used menus. Interactive widgets offer real-time date display, while administrators can manage and publish announcements to improve communication. With Main Menu Odoo App Users can customize their experience by bookmarking internal menus and external links, ensuring effortless navigation. Designed to optimize usability, this module enhances productivity and streamlines the Odoo backend experience.',
    'author': 'Zehntech Technologies Inc.',
    'maintainer': 'Zehntech Technologies Inc.',
    'company': 'Zehntech Technologies Inc.',
    'website': 'https://zehntech.com',
    'depends': ['web'],
    'data': [
        'security/ir.model.access.csv',
        'views/main_menu_views.xml',
        'views/menu_bookmark_views.xml',
        'views/res_config_setting_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'zehntech_main_menu/static/src/components/**/*',
        ],
    },
    'images': [
        'static/description/banner.gif',
    ],
    'license': 'OPL-1',
    'auto_install': False,
    'application': True,
    'installable': True,
}