# -*- coding: utf-8 -*-

from odoo import api, fields, models


class OpticaRxSerie(models.Model):
    _name = "optica.rx.serie"
    _description = "Series RX"
    _order = "sequence, id"

    name = fields.Char(
        string="Serie",
        required=True,
    )

    sequence = fields.Integer(
        string="Secuencia",
        default=10,
    )

    active = fields.Boolean(
        default=True
    )

    description = fields.Text(
        string="Descripción"
    )

    # -------------------------
    # Rangos
    # -------------------------

    sphere_min = fields.Float(
        string="Esfera mínima",
        digits=(6, 2),
        required=True,
    )

    sphere_max = fields.Float(
        string="Esfera máxima",
        digits=(6, 2),
        required=True,
    )

    cylinder_min = fields.Float(
        string="Cilindro mínimo",
        digits=(6, 2),
        required=True,
    )

    cylinder_max = fields.Float(
        string="Cilindro máximo",
        digits=(6, 2),
        required=True,
    )

    addition_min = fields.Float(
        string="Adición mínima",
        digits=(6, 2),
        default=0.00,
    )

    addition_max = fields.Float(
        string="Adición máxima",
        digits=(6, 2),
        default=0.00,
    )

    # -------------------------
    # Métodos
    # -------------------------

    @api.model
    def get_rx_series(self, sphere=0.0, cylinder=0.0, addition=0.0):
        """
        Devuelve la serie RX correspondiente.
        """

        series = self.search(
            [
                ("sphere_min", "<=", sphere),
                ("sphere_max", ">=", sphere),
                ("cylinder_min", "<=", cylinder),
                ("cylinder_max", ">=", cylinder),
                ("addition_min", "<=", addition),
                ("addition_max", ">=", addition),
                ("active", "=", True),
            ],
            order="sequence",
            limit=1,
        )

        return series
