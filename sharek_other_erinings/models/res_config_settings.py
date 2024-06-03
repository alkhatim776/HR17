# -*- coding: utf-8 -*-
from odoo import fields, models, api, exceptions, _

class Company(models.Model):
    _inherit = "res.company"

    credit_account_id = fields.Many2one('account.account', string="Credit Account")
    debit_account_id = fields.Many2one('account.account', string="Debit Account")

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    credit_account_id = fields.Many2one('account.account', related="company_id.credit_account_id", string="Credit Account", readonly=False, store=True)
    debit_account_id = fields.Many2one('account.account', related="company_id.debit_account_id", string="Debit Account", readonly=False, store=True)
