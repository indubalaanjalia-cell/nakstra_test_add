{
    'name': 'Jewellery Management',
     "version": "17.0.1.0.0",
    'category': 'Technical/Technical',
    'sequence': 1,
    'summary': """""",
    'description': '',

    'depends': ['web','base','product','stock','sale','mrp','cr_material_purchase_requisitions','product_combo_pack'],
    'data': [
        'security/ir.model.access.csv',
        'data/jewellery_sequence.xml',
        'views/product_template_view.xml',
        'views/purity_view.xml',
        'views/product_label.xml',
        'views/sale_order.xml',
        'views/job_work.xml',
        'views/res_partner.xml',
        'views/receive_voucher.xml',
        'views/jeweller_menu.xml',
        'views/refinery_menu.xml',
        'views/issue_voucher.xml',
        'views/scheme_view.xml',
        'views/purchase_order.xml',
        'views/requisition_view.xml',
        'views/gold_rate_master_view.xml'

    ],

    'auto_install': False,
    'application': True,
    'installable': True,
}