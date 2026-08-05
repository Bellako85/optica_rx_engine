# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # ==========================================================
    # CLASIFICACIÓN ÓPTICA
    # ==========================================================

    rx_tipo = fields.Selection([
        ('monofocal', 'Monofocal'),
        ('bifocal', 'Bifocal'),
        ('progresivo', 'Progresivo'),
        ('ocupacional', 'Ocupacional'),
        ('contacto', 'Lente de contacto'),
    ], string="Tipo de lente")

    rx_fabricacion = fields.Selection([
        ('terminado', 'Graduación terminada'),
        ('convencional', 'Tallado convencional'),
        ('digital', 'Tallado digital'),
    ], string="Fabricación")

    # ==========================================================
    # SERIES COMPATIBLES
    # ==========================================================

    rx_series_ids = fields.Many2many(
        'optica.rx.serie',
        string='Series compatibles'
    )

    # ==========================================================
    # LABORATORIO
    # ==========================================================

    laboratorio_id = fields.Many2one(
        'res.partner',
        string='Laboratorio',
        domain=[('category_id.name', '=', 'Laboratorio')]
    )

    # ==========================================================
    # MATERIAL
    # ==========================================================

    material_optico = fields.Selection([
        ('cr39', 'CR39'),
        ('poly', 'Policarbonato'),
        ('156', 'Hi-Index 1.56'),
        ('160', 'Hi-Index 1.60'),
        ('167', 'Hi-Index 1.67'),
        ('174', 'Hi-Index 1.74'),
        ('trivex', 'Trivex'),
    ], string="Material")

    # ==========================================================
    # DISEÑO DEL PROGRESIVO
    # ==========================================================

    progresivo_diseno = fields.Selection([
        ('', 'No aplica'),
        ('easy', 'Easy'),
        ('comfort', 'Comfort'),
        ('premium', 'Premium'),
        ('office', 'Office'),
        ('digital', 'Digital'),
        ('elite', 'Elite'),
    ], string="Diseño progresivo")

    # ==========================================================
    # TRATAMIENTO
    # ==========================================================

    tratamiento_ids = fields.Many2many(
        'product.attribute.value',
        string="Tratamientos compatibles"
    )

    # ==========================================================
    # COTIZADOR
    # ==========================================================

    disponible_cotizador = fields.Boolean(
        string="Mostrar en cotizador",
        default=True
    )

    prioridad_cotizador = fields.Integer(
        string="Prioridad",
        default=10,
        help="Entre menor sea el número, primero aparecerá."
    )

    # ==========================================================
    # INFORMACIÓN
    # ==========================================================

    descripcion_cotizador = fields.Text(
        string="Descripción para cotización"
    )

    observaciones_optica = fields.Text(
        string="Observaciones internas"
    )

    # ==========================================================
    # MÉTODO AUXILIAR
    # ==========================================================

    def es_progresivo(self):
        self.ensure_one()
        return self.rx_tipo == 'progresivo'

    def es_bifocal(self):
        self.ensure_one()
        return self.rx_tipo == 'bifocal'

    def es_monofocal(self):
        self.ensure_one()
        return self.rx_tipo == 'monofocal'
