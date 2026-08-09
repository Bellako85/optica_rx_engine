# -*- coding: utf-8 -*-

from odoo import fields, models


class OpticaDiseno(models.Model):
    _name = "optica.diseno"
    _description = "Diseños de Lentes"
    _order = "sequence, name"

    active = fields.Boolean(
        string="Activo",
        default=True
    )

    sequence = fields.Integer(
        string="Secuencia",
        default=10
    )

    name = fields.Char(
        string="Diseño",
        required=True,
        translate=True
    )

    code = fields.Char(
        string="Código"
    )

    laboratorio_id = fields.Many2one(
        'res.partner',
        string='Laboratorio',
        domain=[('es_laboratorio','=',True)],
        ondelete='restrict'
    )

    tipo_lente = fields.Selection([
        ('monofocal', 'Monofocal'),
        ('bifocal', 'Bifocal'),
        ('blend', 'Blend'),
        ('progresivo', 'Progresivo'),
        ('ocupacional', 'Ocupacional'),
    ], string="Tipo de lente", required=True)

    material_ids = fields.Many2many(
        'optica.material',
        string='Materiales compatibles'
    )

    rx_series_ids = fields.Many2many(
        'optica.rx.serie',
        string='Series compatibles'
    )

    prioridad = fields.Integer(
        string='Prioridad',
        default=10
    )

    activo_cotizador = fields.Boolean(
        string='Disponible en Cotizador',
        default=True
    )

    descripcion = fields.Text(
        string='Descripción'
    )

    notes = fields.Text(
        string='Notas internas'
    )

    color = fields.Integer(
        string='Color Kanban'
    )

    _sql_constraints = [
        (
            'diseno_unique',
            'unique(name,laboratorio_id)',
            'Este laboratorio ya tiene un diseño con ese nombre.'
        )
    ]
