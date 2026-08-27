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

    # --------------------------------------------------------
    # OPCIONES DISPONIBLES PROGRESIVO
    # ---------------------------------------------------------

    laboratorios_disponibles_ids = fields.Many2many(
        'res.partner',
        'optica_cotizador_laboratorio_rel',
        'wizard_id',
        'partner_id',
        string='Laboratorios disponibles',
    )

    disenos_disponibles_ids = fields.Many2many(
        'optica.diseno',
        'optica_cotizador_diseno_rel',
        'wizard_id',
        'diseno_id',
        string='Diseños disponibles',
    )

    materiales_disponibles_ids = fields.Many2many(
        'optica.material',
        'optica_cotizador_material_prog_rel',
        'wizard_id',
        'material_id',
        string='Materiales disponibles',
    )

    tratamientos_disponibles_ids = fields.Many2many(
        'product.attribute.value',
        'optica_cotizador_tratamiento_prog_rel',
        'wizard_id',
        'attribute_value_id',
        string='Tratamientos disponibles',
    )
    
    
    serie_od = fields.Char(
        string='Serie OD',
        readonly=True,
    )

    serie_oi = fields.Char(
        string='Serie OI',
        readonly=True,
    )

    # ---------------------------------------------------------
    # CONFIGURACIÓN MONOFOCAL POR OJO
    # ---------------------------------------------------------

    material_od_id = fields.Many2one(
        'product.attribute.value',
        string='Material OD',
    )

    materiales_od_disponibles_ids = fields.Many2many(
        'product.attribute.value',
        'optica_cotizador_material_od_rel',
        'wizard_id',
        'attribute_value_id',
        string='Materiales disponibles OD',
    )

    tratamiento_od_id = fields.Many2one(
        'product.attribute.value',
        string='Tratamiento OD',
    )
    
    tratamientos_od_disponibles_ids = fields.Many2many(
        'product.attribute.value',
        'optica_cotizador_tratamiento_od_rel',
        'wizard_id',
        'attribute_value_id',
        string='Tratamientos disponibles OD',
    )
    
    producto_od_id = fields.Many2one(
        'product.product',
        string='Producto OD',
        readonly=True,
    )

    precio_od = fields.Float(
        string='Precio OD',
        readonly=True,
    )

    material_oi_id = fields.Many2one(
        'product.attribute.value',
        string='Material OI',
    )

    materiales_oi_disponibles_ids = fields.Many2many(
        'product.attribute.value',
        'optica_cotizador_material_oi_rel',
        'wizard_id',
        'attribute_value_id',
        string='Materiales disponibles OI',
    )

    tratamiento_oi_id = fields.Many2one(
        'product.attribute.value',
        string='Tratamiento OI',
    )

    tratamientos_oi_disponibles_ids = fields.Many2many(
        'product.attribute.value',
        'optica_cotizador_tratamiento_oi_rel',
        'wizard_id',
        'attribute_value_id',
        string='Tratamientos disponibles OI',
    )

    producto_oi_id = fields.Many2one(
        'product.product',
        string='Producto OI',
        readonly=True,
    )

    precio_oi = fields.Float(
        string='Precio OI',
        readonly=True,
    )

    precio_total = fields.Float(
        string='Total lentes',
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

            # Campos progresivo/general
            wizard.laboratorios_disponibles_ids = False
            wizard.disenos_disponibles_ids = False
            wizard.materiales_disponibles_ids = False
            wizard.tratamientos_disponibles_ids = False
            wizard.template_id = False
            wizard.producto_id = False
            wizard.precio = 0.0

            # Campos monofocal OD
            wizard.material_od_id = False
            wizard.materiales_od_disponibles_ids = False
            wizard.tratamiento_od_id = False
            wizard.tratamientos_od_disponibles_ids = False
            wizard.producto_od_id = False
            wizard.precio_od = 0.0

            # Campos monofocal OI
            wizard.material_oi_id = False
            wizard.materiales_oi_disponibles_ids = False
            wizard.tratamiento_oi_id = False
            wizard.tratamientos_oi_disponibles_ids = False
            wizard.producto_oi_id = False
            wizard.precio_oi = 0.0

            wizard.precio_total = 0.0

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

                template_mono = self.env['product.template'].browse(409)

                variantes_od = engine.obtener_variantes_por_serie(
                    template_mono,
                    wizard.serie_od,
                )

                variantes_oi = engine.obtener_variantes_por_serie(
                    template_mono,
                    wizard.serie_oi,
                )

                materiales_od = engine.obtener_materiales_desde_variantes(
                    variantes_od
                )

                materiales_oi = engine.obtener_materiales_desde_variantes(
                    variantes_oi
                )

                wizard.materiales_od_disponibles_ids = materiales_od.mapped(
                    'product_attribute_value_id'
                )    

                wizard.materiales_oi_disponibles_ids = materiales_oi.mapped(
                    'product_attribute_value_id'
                )

    @api.onchange('material_od_id')
    def _onchange_material_od_id(self):
        self.tratamiento_od_id = False
        self.producto_od_id = False
        self.precio_od = 0.0
        self.tratamientos_od_disponibles_ids = False

        if not self.material_od_id or not self.serie_od:
            return

        engine = self.env['optica.cotizador.engine']
        template_mono = self.env['product.template'].browse(409)

        variantes = engine.obtener_variantes_por_serie(
            template_mono,
            self.serie_od,
        )

        tratamientos = engine.obtener_tratamientos_desde_variantes(
            variantes,
            self.material_od_id.name,
        )

        self.tratamientos_od_disponibles_ids = tratamientos.mapped(
            'product_attribute_value_id'
        )    


    @api.onchange('material_oi_id')
    def _onchange_material_oi_id(self):
        self.tratamiento_oi_id = False
        self.producto_oi_id = False
        self.precio_oi = 0.0
        self.tratamientos_oi_disponibles_ids = False

        if not self.material_oi_id or not self.serie_oi:
            return

        engine = self.env['optica.cotizador.engine']
        template_mono = self.env['product.template'].browse(409)

        variantes = engine.obtener_variantes_por_serie(
            template_mono,
            self.serie_oi,
        )

        tratamientos = engine.obtener_tratamientos_desde_variantes(
            variantes,
            self.material_oi_id.name,
        )

        self.tratamientos_oi_disponibles_ids = tratamientos.mapped(
            'product_attribute_value_id'
        )

    @api.onchange('tratamiento_od_id')
    def _onchange_tratamiento_od_id(self):
        self.producto_od_id = False
        self.precio_od = 0.0

        if not (
            self.serie_od
            and self.material_od_id
            and self.tratamiento_od_id
        ):
            self._actualizar_total_monofocal()
            return

        engine = self.env['optica.cotizador.engine']
        template_mono = self.env['product.template'].browse(409)

        producto = engine.buscar_variante_exacta(
            template_mono,
            self.serie_od,
            self.material_od_id.name,
            self.tratamiento_od_id.name,
        )

        self.producto_od_id = producto[:1]

        if self.producto_od_id:
            self.precio_od = self.producto_od_id.lst_price

        self._actualizar_total_monofocal()


    @api.onchange('tratamiento_oi_id')
    def _onchange_tratamiento_oi_id(self):
        self.producto_oi_id = False
        self.precio_oi = 0.0

        if not (
            self.serie_oi
            and self.material_oi_id
            and self.tratamiento_oi_id
        ):
            self._actualizar_total_monofocal()
            return

        engine = self.env['optica.cotizador.engine']
        template_mono = self.env['product.template'].browse(409)

        producto = engine.buscar_variante_exacta(
            template_mono,
            self.serie_oi,
            self.material_oi_id.name,
            self.tratamiento_oi_id.name,
        )

        self.producto_oi_id = producto[:1]

        if self.producto_oi_id:
            self.precio_oi = self.producto_oi_id.lst_price

        self._actualizar_total_monofocal()
            
    def _actualizar_total_monofocal(self):
        for wizard in self:
            wizard.precio_total = (
                (wizard.precio_od or 0.0)
                + (wizard.precio_oi or 0.0)
            )
    
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

        self.laboratorios_disponibles_ids = False
        self.disenos_disponibles_ids = False
        self.materiales_disponibles_ids = False
        self.tratamientos_disponibles_ids = False
        
        if self.subtipo != 'progresivo':
            return

        engine = self.env['optica.cotizador.engine']

        laboratorios = engine.obtener_laboratorios(
            'multifocal',
            'progresivo',
        )

        self.laboratorios_disponibles_ids = laboratorios
    
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

        self.disenos_disponibles_ids = False
        self.materiales_disponibles_ids = False
        self.tratamientos_disponibles_ids = False

        if not self.laboratorio_id:
            return

        engine = self.env['optica.cotizador.engine']

        disenos = engine.obtener_disenos(
            'multifocal',
            self.laboratorio_id,
            'progresivo',
        )

        self.disenos_disponibles_ids = disenos

    # ---------------------------------------------------------
    # MATERIAL
    # ---------------------------------------------------------

    @api.onchange('diseno_id')
    def _onchange_diseno_id(self):
        self.material_id = False
        self.tratamiento_id = False
        self.template_id = False
        self.producto_id = False

        self.materiales_disponibles_ids = False
        self.tratamientos_disponibles_ids = False

        if not self.diseno_id or not self.laboratorio_id:
            return

        templates = self.env['product.template'].search([
            ('rx_tipo', '=', 'progresivo'),
            ('laboratorio_id', '=', self.laboratorio_id.id),
            ('diseno_id', '=', self.diseno_id.id),
            ('disponible_cotizador', '=', True),
        ])

        materiales = templates.mapped('material_id')

        self.materiales_disponibles_ids = materiales

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

        self.tratamientos_disponibles_ids = tratamientos

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
