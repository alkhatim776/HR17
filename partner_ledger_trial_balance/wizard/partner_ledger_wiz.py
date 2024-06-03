# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

import io
from io import BytesIO
import xlsxwriter
from num2words import num2words

from PIL import Image
import base64



class Accounting_reportPartner_ledger(models.TransientModel):
    _name = "partnerledger.wiz"

    company_id = fields.Many2one('res.company', string='Company', readonly=False,
                                 default=lambda self: self.env.company)
    date_from = fields.Date(string='Start Date', default=lambda self: fields.Date.context_today(self).replace(month=1, day=1))
    date_to = fields.Date(string='End Date', default= lambda self: fields.Date.context_today(self).replace(month=12, day=31))
    target_move = fields.Selection([('posted', 'All Posted Entries'),
                                    ('all', 'All Entries'),
                                    ], string='Target Moves', required=True, default='posted')
    reconciled = fields.Boolean('Show Initial Balance', default=True)
    result_selection = fields.Selection([('customer', 'Receivable Accounts'),
                                         ('supplier', 'Payable Accounts'),
                                         ('customer_supplier', 'Receivable and Payable Accounts')
                                         ], string="Account Type", required=True, default='customer_supplier')
    partner_ids = fields.Many2many('res.partner','rel_multicurrency_partner',
                                   'multicurrency_id','partner_id', change_default=True,
                                   string="Partner's")
    account_ids = fields.Many2many('account.account', string='Accounts')
    partner_tag_ids = fields.Many2many('res.partner.category', string='Partner Tags')
    options = fields.Selection([('total', 'Total'),
                                ('detailed', 'Detailed'),
                            ], string="Options", required=True, default='detailed')
  
    
    
    def export_xls_report(self):
        data = self.read()[0]
        used_context = {}
        data['move_state'] = ['draft', 'posted']
        if self.target_move == 'posted':
            data['move_state'] = ['posted']

        return self.env.ref('partner_ledger_trial_balance.action_partner_ledger_xls').with_context(
                    used_context).report_action(self, data=data)
    
    def view_report(self):
        data = self.read()[0]
        used_context = {}
        data['move_state'] = ['draft', 'posted']
        if self.target_move == 'posted':
            data['move_state'] = ['posted']
        if self.options == 'total':
            return self.env.ref('partner_ledger_trial_balance.partner_ledger_html').with_context(
                    used_context).report_action(self, data=data)
        else:
            return self.env.ref('partner_ledger_trial_balance.partner_ledger_details_html').with_context(
                used_context).report_action(self, data=data)
    
    
    def print_partner_ledger(self):
        data = self.read()[0]
        used_context = {}
        data['move_state'] = ['draft', 'posted']
        if self.target_move == 'posted':
            data['move_state'] = ['posted']
        if self.options == 'total':
            return self.env.ref('partner_ledger_trial_balance.partner_ledger').with_context(
                        used_context).report_action(self, data=data)
        else:
            return self.env.ref('partner_ledger_trial_balance.partner_ledger_details').with_context(
                        used_context).report_action(self, data=data)
        