{
    'name': 'Jewellery Management',
     "version": "17.0.1.0.0",
    'category': 'Technical/Technical',
    'sequence': 1,
    'summary': """""",
    'description': '',

    'depends': ['web','base','product','stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_view.xml',
        'views/purity_view.xml',
    ],

    'auto_install': False,
    'application': True,
    'installable': True,
}