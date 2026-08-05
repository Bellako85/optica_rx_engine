# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # ==========================================================
    # LABORATORIOS
    # ==========================================================

    es_laboratorio = fields.Boolean(
        string="Es laboratorio"
    )

    activo_cotizador = fields.Boolean(
        string="Disponible en Cotizador",
        default=True
    )

    prioridad_cotizador = fields.Integer(
        string="Prioridad",
        default=10
    )

    # ==========================================================
    # FABRICACIÓN
    # ==========================================================

    fabrica_monofocal = fields.Boolean(
        string="Monofocal",
        default=True
    )

    fabrica_bifocal = fields.Boolean(
        string="Bifocal"
    )

    fabrica_progresivo = fields.Boolean(
        string="Progresivo"
    )

    fabrica_digital = fields.Boolean(
        string="Tallado Digital"
    )

    fabrica_convencional = fields.Boolean(
        string="Tallado Convencional"
    )

    # ==========================================================
    # LOGÍSTICA
    # ==========================================================

    dias_entrega = fields.Integer(
        string="Días de entrega",
        default=5
    )

    pedido_minimo = fields.Float(
        string="Pedido mínimo"
    )

    email_pedidos = fields.Char(
        string="Correo para pedidos"
    )

    whatsapp = fields.Char(
        string="WhatsApp"
    )

    sitio_pedidos = fields.Char(
        string="Portal de pedidos"
    )

    observaciones_lab = fields.Text(
        string="Observaciones"
    )
