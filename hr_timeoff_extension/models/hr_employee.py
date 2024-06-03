# -*- coding: utf-8 -*-

from odoo import fields, models, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    religion_id = fields.Many2one('religion.religion', string='Religion')
