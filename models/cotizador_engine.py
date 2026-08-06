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
        Determina si la graduación es:

        - Monofocal
        - Multifocal

        La decisión entre Bifocal o Progresivo
        la toma posteriormente el usuario.
        """

        pass

    # ==========================================================
    # PASO 2
    # ==========================================================

    @api.model
    def determinar_serie(self, graduacion):
        """
        Determina la serie RX
        para fabricación convencional.
        """

        pass

    # ==========================================================
    # PASO 3
    # ==========================================================

    @api.model
    def obtener_materiales(
        self,
        graduacion,
        tipo,
        serie
    ):
        """
        Devuelve los materiales compatibles.
        """

        pass

    # ==========================================================
    # PASO 4
    # ==========================================================

    @api.model
    def obtener_laboratorios(
        self,
        graduacion,
        tipo,
        serie,
        materiales
    ):
        """
        Busca los laboratorios
        compatibles con la cotización.
        """

        pass

    # ==========================================================
    # PASO 5
    # ==========================================================

    @api.model
    def obtener_disenos(
        self,
        graduacion,
        tipo,
        laboratorios
    ):
        """
        Devuelve los diseños
        disponibles para el laboratorio.
        """

        pass

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
