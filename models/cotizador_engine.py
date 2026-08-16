# -*- coding: utf-8 -*-

from odoo import api, models


class OpticaCotizadorEngine(models.AbstractModel):
    _name = "optica.cotizador.engine"
    _description = "Motor Inteligente del Cotizador Óptico"

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
        se realiza posteriormente por el usuario.
        """

        if not graduacion:
            return False

        if graduacion.adicion and graduacion.adicion > 0:
            return "multifocal"

        return "monofocal"

    # ==========================================================
    # PASO 2
    # ==========================================================

    @api.model
    def determinar_serie(self, graduacion):
        """
        Obtiene las series RX que ya fueron calculadas
        por el módulo de graduaciones.

        No recalcula la serie.

        Devuelve la serie recomendada para:
            OD = ojo derecho
            OI = ojo izquierdo
        """

        if not graduacion:
            return False

        return {
            "od": graduacion.serie_recomendada_od,
            "oi": graduacion.serie_recomendada_oi,
        }

    
    # ==========================================================
    # PASO 2.1 - VARIANTES COMPATIBLES CON LA SERIE
    # ==========================================================

    @api.model
    def obtener_variantes_por_serie(self, template, serie_rx):
        """
        Obtiene las variantes reales del producto compatibles
        con una serie RX previamente calculada por graduacion.py.

        NO calcula la serie.

        Traduce:
            RX1 -> 1ª SERIE
            RX2 -> 2ª SERIE
            RX3 -> 3ª SERIE
        """

        ProductProduct = self.env['product.product']

        if not template or not serie_rx:
            return ProductProduct

        mapa_series = {
            'RX1': '1ª SERIE',
            'RX2': '2ª SERIE',
            'RX3': '3ª SERIE',
        }

        nombre_serie = mapa_series.get(serie_rx)

        if not nombre_serie:
            return ProductProduct

        return template.product_variant_ids.filtered(
            lambda variante: any(
                valor.attribute_id.name == 'SERIE'
                and valor.name == nombre_serie
                for valor in variante.product_template_attribute_value_ids
            )
        )
    

    @api.model
    def obtener_materiales_desde_variantes(self, variantes):
        """
        Obtiene los materiales únicos disponibles
        a partir de un conjunto de variantes válidas.

        No inventa materiales ni recalcula compatibilidades.
        Solo lee los valores reales del atributo
        'MICA GRADUADA' presentes en product.product.
        """

        if not variantes:
            return self.env['product.template.attribute.value']

        materiales = variantes.mapped(
            'product_template_attribute_value_ids'
        ).filtered(
            lambda valor: valor.attribute_id.name == 'MATERIAL'
        )

        return materiales

    @api.model
    def obtener_tratamientos_desde_variantes(self, variantes, material):
        """
        Devuelve los tratamientos disponibles para un material
        dentro de un conjunto de variantes válidas.

        material puede ser:
            - un registro product.template.attribute.value
            - o el nombre del material
        """

        if not variantes or not material:
            return self.env['product.template.attribute.value']

        nombre_material = (
            material.name
            if hasattr(material, 'name')
            else material
        )

        variantes_material = variantes.filtered(
            lambda variante: any(
                valor.attribute_id.name == 'MATERIAL'
                and valor.name == nombre_material
                for valor in variante.product_template_attribute_value_ids
            )
        )

        tratamientos = variantes_material.mapped(
            'product_template_attribute_value_ids'
        ).filtered(
            lambda valor: valor.attribute_id.name == 'TRATAMIENTO'
        )

        return tratamientos
    
    # ==========================================================
    # PASO 3
    # ==========================================================

    @api.model
    def obtener_materiales(self, tipo_lente, serie=None):
        """
        Obtiene los materiales compatibles con el tipo
        general de lente.

        La serie se recibe para futuras reglas de
        compatibilidad.
        """

        Material = self.env["optica.material"]

        if not tipo_lente:
            return Material.browse()

        dominio = [
            ("active", "=", True),
        ]

        # ------------------------------------------------------
        # MONOFOCAL
        # ------------------------------------------------------

        if tipo_lente == "monofocal":
            dominio.append(
                ("monofocal", "=", True)
            )

        # ------------------------------------------------------
        # MULTIFOCAL
        # ------------------------------------------------------

        elif tipo_lente == "multifocal":
            dominio += [
                "|",
                ("bifocal", "=", True),
                ("progresivo", "=", True),
            ]

        return Material.search(
            dominio,
            order="sequence, name"
        )

    # ==========================================================
    # PASO 4
    # ==========================================================

    @api.model
    def obtener_laboratorios(self, tipo_lente, subtipo=None):
        """
        Obtiene los laboratorios compatibles.

        Monofocal:
            No requiere laboratorio.

        Multifocal:
            subtipo = bifocal
            subtipo = progresivo
        """

        Partner = self.env["res.partner"]

        # ------------------------------------------------------
        # MONOFOCAL
        # ------------------------------------------------------

        if tipo_lente == "monofocal":
            return Partner.browse()

        # ------------------------------------------------------
        # MULTIFOCAL
        # ------------------------------------------------------

        if tipo_lente != "multifocal":
            return Partner.browse()

        dominio = [
            ("es_laboratorio", "=", True),
            ("activo_cotizador", "=", True),
        ]

        # ------------------------------------------------------
        # BIFOCAL
        # ------------------------------------------------------

        if subtipo == "bifocal":
            dominio.append(
                ("fabrica_bifocal", "=", True)
            )

        # ------------------------------------------------------
        # PROGRESIVO
        # ------------------------------------------------------

        elif subtipo == "progresivo":
            dominio.append(
                ("fabrica_progresivo", "=", True)
            )

        else:
            # Todavía no se ha seleccionado
            # bifocal o progresivo.
            return Partner.browse()

        return Partner.search(
            dominio,
            order="prioridad_cotizador, name"
        )

    # ==========================================================
    # PASO 5
    # ==========================================================

    @api.model
    def obtener_disenos(
        self,
        tipo_lente,
        laboratorio=None,
        subtipo=None,
    ):
        """
        Obtiene los diseños disponibles.

        Se filtran por:
            - Activo
            - Disponible en cotizador
            - Tipo de lente
            - Laboratorio

        Para multifocal:
            el subtipo determina si buscamos
            bifocal o progresivo.
        """

        Diseno = self.env["optica.diseno"]

        if not tipo_lente:
            return Diseno.browse()

        dominio = [
            ("active", "=", True),
            ("activo_cotizador", "=", True),
        ]

        # ------------------------------------------------------
        # TIPO DE LENTE
        # ------------------------------------------------------

        if tipo_lente == "monofocal":
            dominio.append(
                ("tipo_lente", "=", "monofocal")
            )

        elif tipo_lente == "multifocal":

            if subtipo not in ("bifocal", "progresivo"):
                return Diseno.browse()

            dominio.append(
                ("tipo_lente", "=", subtipo)
            )

        else:
            dominio.append(
                ("tipo_lente", "=", tipo_lente)
            )

        # ------------------------------------------------------
        # LABORATORIO
        # ------------------------------------------------------

        if laboratorio:
            dominio.append(
                ("laboratorio_id", "=", laboratorio.id)
            )

        return Diseno.search(
            dominio,
            order="prioridad, sequence, name"
        )

    # ==========================================================
    # PASO 6
    # ==========================================================

    @api.model
    def obtener_productos(
        self,
        tipo_lente,
        material=None,
        laboratorio=None,
        diseno=None,
        serie=None,
    ):
        """
        Obtiene los productos compatibles con la
        configuración seleccionada.

        tipo_lente puede ser:

            monofocal
            bifocal
            progresivo
            blend
            ocupacional

        Importante:
            'multifocal' es una clasificación interna
            del motor y NO es un valor de rx_tipo.
        """

        Product = self.env["product.template"]

        if not tipo_lente:
            return Product.browse()

        # ------------------------------------------------------
        # MULTIFOCAL
        # ------------------------------------------------------

        # Si todavía tenemos la clasificación general
        # multifocal, todavía no podemos buscar productos,
        # porque falta decidir bifocal o progresivo.

        if tipo_lente == "multifocal":
            return Product.browse()

        dominio = [
            ("sale_ok", "=", True),
            ("disponible_cotizador", "=", True),
            ("rx_tipo", "=", tipo_lente),
        ]

        # ------------------------------------------------------
        # MATERIAL
        # ------------------------------------------------------

        if material:
            dominio.append(
                ("material_id", "=", material.id)
            )

        # ------------------------------------------------------
        # LABORATORIO
        # ------------------------------------------------------

        if laboratorio:
            dominio.append(
                ("laboratorio_id", "=", laboratorio.id)
            )

        # ------------------------------------------------------
        # DISEÑO
        # ------------------------------------------------------

        if diseno:
            dominio.append(
                ("diseno_id", "=", diseno.id)
            )

        # ------------------------------------------------------
        # SERIE RX
        # ------------------------------------------------------

        if serie:

            Serie = self.env["optica.rx.serie"]

            # --------------------------------------------------
            # Registro de serie
            # --------------------------------------------------

            if hasattr(serie, "id"):
                if serie.id:
                    dominio.append(
                        ("rx_series_ids", "in", serie.id)
                    )

            # --------------------------------------------------
            # Nombre de serie
            # --------------------------------------------------

            elif isinstance(serie, str):

                serie_record = Serie.search(
                    [
                        ("name", "=", serie),
                        ("active", "=", True),
                    ],
                    limit=1,
                )

                if serie_record:
                    dominio.append(
                        (
                            "rx_series_ids",
                            "in",
                            serie_record.id,
                        )
                    )

        return Product.search(
            dominio,
            order="prioridad_cotizador, name"
        )

    # ==========================================================
    # FLUJO AUTOMÁTICO INICIAL
    # ==========================================================

    @api.model
    def cotizar(self, graduacion):
        """
        Primera etapa del cotizador.

        Aquí solamente resolvemos lo que puede determinarse
        automáticamente a partir de la graduación.

        Devuelve:

            tipo
            serie
            materiales

        Si es multifocal, el usuario deberá seleccionar
        posteriormente bifocal o progresivo.
        """

        if not graduacion:
            return {
                "tipo": False,
                "serie": False,
                "materiales": self.env["optica.material"].browse(),
            }

        tipo = self.determinar_tipo_lente(
            graduacion
        )

        serie = self.determinar_serie(
            graduacion
        )

        materiales = self.obtener_materiales(
            tipo,
            serie
        )

        return {
            "tipo": tipo,
            "serie": serie,
            "materiales": materiales,
        }
