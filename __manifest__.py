# -*- coding: utf-8 -*-

{
    'name': 'Optica RX Engine',
    'version': '17.0.1.0.0',
    'category': 'Sales',
    'summary': 'Motor de reglas para cotización óptica',
    'author': 'Optica Zamora',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'product',
        'odoo_graduacion_paciente',
    ],

    'data': [
        'views/cotizador_wizard_views.xml',
    ],
    
    'installable': True,
    'application': True,
}
