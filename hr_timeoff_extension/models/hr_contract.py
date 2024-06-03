# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Contract(models.Model):
    _inherit = 'hr.contract'
    _description = 'Contract Extension'

    timeoff_days = fields.Integer('Timeoff Days')
    timeoff_type = fields.Many2one('hr.leave.type', domain="[('is_annual', '=', True)]")

