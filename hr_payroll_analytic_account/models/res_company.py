# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResCompany(models.Model):
    _inherit = "res.company"
    
    restrict_analytic_account = fields.Boolean('Restrict Analytic Account for Accounts')
    account_type_ids = fields.Many2many('account.type.selection', string='Restricted Account Types')