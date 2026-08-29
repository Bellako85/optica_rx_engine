# -*- coding: utf-8 -*-

{
    'name': 'Optica RX Engine',
    'version': '17.0.1.0.0',
    'category': 'Sales',
    'summary': 'Motor de reglas para cotización óptica',
    'author': 'Christian Torres Optica Zamora',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'product',
        'odoo_graduacion_paciente',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/cotizador_wizard_views.xml',
        'views/product_template_views.xml',
    ],

    'assets': {
        'web.assets_backend': [
            'optica_rx_engine/static/src/css/cotizador_wizard.css',
    ],
},
    
    'installable': True,
    'application': True,
}
