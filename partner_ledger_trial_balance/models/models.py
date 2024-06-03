# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class aktan_partner_ledger_trial_balance(models.Model):
#     _name = 'aktan_partner_ledger_trial_balance.aktan_partner_ledger_trial_balance'
#     _description = 'aktan_partner_ledger_trial_balance.aktan_partner_ledger_trial_balance'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
