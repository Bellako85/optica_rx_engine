# -*- coding: utf-8 -*-

from odoo import fields, models


class OpticaMaterial(models.Model):
    _name = "optica.material"
    _description = "Materiales Ópticos"
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
        string="Material",
        required=True,
        translate=True
    )

    code = fields.Char(
        string="Código",
        help="Código interno del material."
    )

    description = fields.Text(
        string="Descripción"
    )

    # Índice de refracción
    refractive_index = fields.Float(
        string="Índice de refracción",
        digits=(4, 2)
    )

    # Densidad
    density = fields.Float(
        string="Densidad",
        digits=(6, 3)
    )

    # Compatible con
    monofocal = fields.Boolean(
        string="Monofocal",
        default=True
    )

    bifocal = fields.Boolean(
        string="Bifocal",
        default=True
    )

    blend = fields.Boolean(
        string="Blend",
        default=True
    )

    progresivo = fields.Boolean(
        string="Progresivo",
        default=True
    )

    ocupacional = fields.Boolean(
        string="Ocupacional"
    )

    contacto = fields.Boolean(
        string="Lente de contacto"
    )

    notes = fields.Text(
        string="Notas"
    )

    color = fields.Integer(
        string="Color Kanban"
    )

    _sql_constraints = [
        (
            'material_name_unique',
            'unique(name)',
            'Ya existe un material con ese nombre.'
        )
    ]
