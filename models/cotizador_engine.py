# -*- coding: utf-8 -*-

from odoo import models, api


class OpticaCotizadorEngine(models.AbstractModel):
    _name = "optica.cotizador.engine"
    _description = "Motor Inteligente del Cotizador Óptico"

    # ==========================================================
    # MÉTODO PRINCIPAL
    # ==========================================================

    @api.model
    def cotizar(self, graduacion):
        """
        Punto de entrada del motor.
        """

        tipo = self.determinar_tipo_lente(graduacion)

        serie = self.determinar_serie(graduacion)

        materiales = self.obtener_materiales(
            graduacion,
            tipo,
            serie
        )

        laboratorios = self.obtener_laboratorios(
            graduacion,
            tipo,
            serie,
            materiales
        )

        disenos = self.obtener_disenos(
            graduacion,
            tipo,
            laboratorios
        )

        productos = self.obtener_productos(
            graduacion,
            tipo,
            serie,
            materiales,
            laboratorios,
            disenos
        )

        return {
            "tipo": tipo,
            "serie": serie,
            "materiales": materiales,
            "laboratorios": laboratorios,
            "disenos": disenos,
            "productos": productos,
        }

    # ==========================================================
    # PASO 1
    # ==========================================================

    @api.model
    def determinar_tipo_lente(self, graduacion):
    """
    Determina el tipo general de lente.

    Sin adición:
        monofocal

    Con adición:
        multifocal

    La elección entre bifocal y progresivo
    se hará posteriormente en el cotizador.
    """

    if not graduacion:
        return False

    if graduacion.adicion and graduacion.adicion > 0:
        return 'multifocal'

    return 'monofocal'

    # ==========================================================
    # PASO 2
    # ==========================================================

    @api.model
    def determinar_serie(self, graduacion):
    """
    Obtiene las series RX que ya fueron calculadas
    por el módulo de graduaciones.

    Se conserva la serie de cada ojo por separado:
        - OD = ojo derecho
        - OI = ojo izquierdo

    El cotizador no recalcula las series.
    """

    if not graduacion:
        return False

    return {
        'od': graduacion.serie_recomendada_od,
        'oi': graduacion.serie_recomendada_oi,
    }

    # ==========================================================
    # PASO 3
    # ==========================================================

    @api.model
    def obtener_materiales(self, tipo_lente, serie=None):
    """
    Obtiene los materiales compatibles con el tipo de lente.

    La serie se recibe para futuras reglas de compatibilidad,
    pero por ahora el material se filtra únicamente por
    el tipo de lente.
    """

    if not tipo_lente:
        return self.env['optica.material']

    dominio = [
        ('active', '=', True),
    ]

    if tipo_lente == 'monofocal':
        dominio.append(('monofocal', '=', True))

    elif tipo_lente == 'multifocal':
        # Multifocal significa que posteriormente el usuario
        # podrá elegir Bifocal o Progresivo.
        dominio += [
            '|',
            ('bifocal', '=', True),
            ('progresivo', '=', True),
        ]

    return self.env['optica.material'].search(
        dominio,
        order='sequence, name'
    )

    # ==========================================================
    # PASO 4
    # ==========================================================

    @api.model
    def obtener_laboratorios(self, tipo_lente, subtipo=None):
    """
    Obtiene los laboratorios compatibles con el tipo de lente.

    Parámetros:
        tipo_lente:
            monofocal / multifocal

        subtipo:
            bifocal / progresivo

    Reglas:
        - Monofocal: no necesita seleccionar laboratorio.
        - Bifocal: laboratorios que fabriquen bifocal.
        - Progresivo: laboratorios que fabriquen progresivo.
    """

    # ------------------------------------------------------
    # MONOFOCAL
    # ------------------------------------------------------

    if tipo_lente == 'monofocal':
        return self.env['res.partner'].browse()

    # ------------------------------------------------------
    # MULTIFOCAL
    # ------------------------------------------------------

    if tipo_lente != 'multifocal':
        return self.env['res.partner'].browse()

    dominio = [
        ('es_laboratorio', '=', True),
        ('activo_cotizador', '=', True),
    ]

    # ------------------------------------------------------
    # BIFOCAL
    # ------------------------------------------------------

    if subtipo == 'bifocal':
        dominio.append(
            ('fabrica_bifocal', '=', True)
        )

    # ------------------------------------------------------
    # PROGRESIVO
    # ------------------------------------------------------

    elif subtipo == 'progresivo':
        dominio.append(
            ('fabrica_progresivo', '=', True)
        )

    return self.env['res.partner'].search(
        dominio,
        order='prioridad_cotizador, name'
    )

    # ==========================================================
    # PASO 5
    # ==========================================================

    @api.model
    def obtener_disenos(self, tipo_lente, laboratorio=None):
    """
    Obtiene los diseños disponibles para el tipo de lente
    y laboratorio seleccionado.

    Los diseños deben estar:
        - Activos
        - Disponibles en el cotizador
        - Asociados al tipo de lente solicitado

    Para multifocales:
        el laboratorio seleccionado es obligatorio.
    """

    if not tipo_lente:
        return self.env['optica.diseno']

    dominio = [
        ('active', '=', True),
        ('activo_cotizador', '=', True),
        ('tipo_lente', '=', tipo_lente),
    ]

    # ------------------------------------------------------
    # LABORATORIO
    # ------------------------------------------------------

    if laboratorio:
        dominio.append(
            ('laboratorio_id', '=', laboratorio.id)
        )

    return self.env['optica.diseno'].search(
        dominio,
        order='prioridad, sequence, name'
    )

    # ==========================================================
    # PASO 6
    # ==========================================================

    @api.model
    def obtener_productos(
        self,
        graduacion,
        tipo,
        serie,
        materiales,
        laboratorios,
        disenos
    ):
        """
        Devuelve los productos
        finales para cotizar.
        """

        pass
