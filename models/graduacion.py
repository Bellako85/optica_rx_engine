# -*- coding: utf-8 -*-

from odoo import models


class OpticaGraduacion(models.Model):
    _inherit = 'optica.graduacion'

    def action_cotizar_lentes(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Cotizador Óptico',
            'res_model': 'optica.cotizador.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_graduacion_id': self.id,
            },
        }
