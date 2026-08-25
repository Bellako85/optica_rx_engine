# -*- coding: utf-8 -*-

from odoo import api, fields, models


class OpticaCotizadorWizard(models.TransientModel):
    _name = 'optica.cotizador.wizard'
    _description = 'Cotizador Óptico'

    graduacion_id = fields.Many2one(
        'optica.graduacion',
        string='Graduación',
        required=True,
    )

    tipo_general = fields.Selection([
        ('monofocal', 'Monofocal'),
        ('multifocal', 'Multifocal'),
    ], string='Tipo general', readonly=True)

    serie_od = fields.Char(
        string='Serie OD',
        readonly=True,
    )

    serie_oi = fields.Char(
        string='Serie OI',
        readonly=True,
    )

    subtipo = fields.Selection([
        ('bifocal', 'Bifocal'),
        ('progresivo', 'Progresivo'),
    ], string='Tipo de lente')

    laboratorio_id = fields.Many2one(
        'res.partner',
        string='Laboratorio',
    )

    diseno_id = fields.Many2one(
        'optica.diseno',
        string='Diseño',
    )

    material_id = fields.Many2one(
        'optica.material',
        string='Material',
    )

    tratamiento_id = fields.Many2one(
        'product.attribute.value',
        string='Tratamiento',
    )

    template_id = fields.Many2one(
        'product.template',
        string='Producto base',
        readonly=True,
    )

    producto_id = fields.Many2one(
        'product.product',
        string='Producto final',
        readonly=True,
    )

    precio = fields.Float(
        string='Precio',
        readonly=True,
    )

    # ---------------------------------------------------------
    # GRADUACIÓN
    # ---------------------------------------------------------

    @api.onchange('graduacion_id')
    def _onchange_graduacion_id(self):
        for wizard in self:
            wizard.tipo_general = False
            wizard.subtipo = False
            wizard.serie_od = False
            wizard.serie_oi = False
            wizard.laboratorio_id = False
            wizard.diseno_id = False
            wizard.material_id = False
            wizard.tratamiento_id = False
            wizard.template_id = False
            wizard.producto_id = False
            wizard.precio = 0.0

            if not wizard.graduacion_id:
                continue

            engine = self.env['optica.cotizador.engine']

            wizard.tipo_general = engine.determinar_tipo_lente(
                wizard.graduacion_id
            )

            if wizard.tipo_general == 'monofocal':
                series = engine.determinar_serie(
                    wizard.graduacion_id
                )

                wizard.serie_od = series.get('od')
                wizard.serie_oi = series.get('oi')

    # ---------------------------------------------------------
    # LABORATORIOS
    # ---------------------------------------------------------

    @api.onchange('subtipo')
    def _onchange_subtipo(self):
        self.laboratorio_id = False
        self.diseno_id = False
        self.material_id = False
        self.tratamiento_id = False
        self.template_id = False
        self.producto_id = False

        if self.subtipo != 'progresivo':
            return

        engine = self.env['optica.cotizador.engine']

        laboratorios = engine.obtener_laboratorios(
            'multifocal',
            'progresivo',
        )

        return {
            'domain': {
                'laboratorio_id': [
                    ('id', 'in', laboratorios.ids)
                ]
            }
        }

    # ---------------------------------------------------------
    # DISEÑOS
    # ---------------------------------------------------------

    @api.onchange('laboratorio_id')
    def _onchange_laboratorio_id(self):
        self.diseno_id = False
        self.material_id = False
        self.tratamiento_id = False
        self.template_id = False
        self.producto_id = False

        if not self.laboratorio_id:
            return

        engine = self.env['optica.cotizador.engine']

        disenos = engine.obtener_disenos(
            'multifocal',
            self.laboratorio_id,
            'progresivo',
        )

        return {
            'domain': {
                'diseno_id': [
                    ('id', 'in', disenos.ids)
                ]
            }
        }

    # ---------------------------------------------------------
    # MATERIAL
    # ---------------------------------------------------------

    @api.onchange('diseno_id')
    def _onchange_diseno_id(self):
        self.material_id = False
        self.tratamiento_id = False
        self.template_id = False
        self.producto_id = False

        if not self.diseno_id or not self.laboratorio_id:
            return

        templates = self.env['product.template'].search([
            ('rx_tipo', '=', 'progresivo'),
            ('laboratorio_id', '=', self.laboratorio_id.id),
            ('diseno_id', '=', self.diseno_id.id),
            ('disponible_cotizador', '=', True),
        ])

        materiales = templates.mapped('material_id')

        return {
            'domain': {
                'material_id': [
                    ('id', 'in', materiales.ids)
                ]
            }
        }

    # ---------------------------------------------------------
    # TEMPLATE + TRATAMIENTOS
    # ---------------------------------------------------------

    @api.onchange('material_id')
    def _onchange_material_id(self):
        self.tratamiento_id = False
        self.template_id = False
        self.producto_id = False
        self.precio = 0.0

        if not (
            self.laboratorio_id
            and self.diseno_id
            and self.material_id
        ):
            return

        engine = self.env['optica.cotizador.engine']

        template = engine.buscar_template_progresivo(
            self.laboratorio_id,
            self.diseno_id,
            self.material_id,
        )

        self.template_id = template

        if not template:
            return

        tratamientos = engine.obtener_tratamientos_template(
            template
        )

        return {
            'domain': {
                'tratamiento_id': [
                    ('id', 'in', tratamientos.ids)
                ]
            }
        }

    # ---------------------------------------------------------
    # VARIANTE FINAL
    # ---------------------------------------------------------

    @api.onchange('tratamiento_id')
    def _onchange_tratamiento_id(self):
        self.producto_id = False
        self.precio = 0.0

        if not self.template_id or not self.tratamiento_id:
            return

        engine = self.env['optica.cotizador.engine']

        producto = engine.obtener_o_crear_variante_progresivo(
            self.template_id,
            self.tratamiento_id,
        )

        self.producto_id = producto

        if producto:
            self.precio = producto.lst_price
