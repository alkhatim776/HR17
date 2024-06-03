# -*- coding: utf-8 -*-

from odoo import api, models, fields, _
from odoo.tools.misc import get_lang


class ReportPartnerLedger(models.AbstractModel):
    _name = 'report.partner_ledger_trial_balance.report_partnerledger'

    def get_where(self, data, intial=False):
        
        wheres = f" where move.state in {tuple(data['move_state'])+('non',)}"
        
        company_ids = self._context.get('allowed_company_ids',[data['company_id'][0]])
        wheres += f" and ml.company_id in {tuple(company_ids)+(0,)} "
        account_type = data['result_selection']
        if account_type == ['supplier']:
            account_type = ['liability_payable']
        elif account_type == ['customer']:
            account_type = ['asset_receivable']
        else:
            account_type = ['asset_receivable', 'liability_payable']
        if data['account_ids']:
            wheres += f" and account.id in {tuple(data['account_ids'])+(0,)} "
        else:
            wheres += f" and account.account_type in {tuple(account_type)+('0',)}"
        
        if data['partner_ids']:
            wheres += f" and ml.partner_id in {tuple(data['partner_ids'])+(0,)} "
        
        if data['partner_tag_ids']:
            wheres += f" and tag.id in {tuple(data['partner_tag_ids'])+(0,)} "
        
        return wheres
    
    def get_joins(self,data):
        
        joins = f""
        
        if data['partner_tag_ids']:
            joins += f""" join res_partner_res_partner_category_rel as partner_tag_com on partner_tag_com.partner_id = ml.partner_id 
            join res_partner_category as tag on tag.id = partner_tag_com.category_id """
            
        
        return joins
    
    
    def get_data(self, data, wheres, joins):
        ''
        date_from = data['date_from'] or "2001-01-01"        
        date_to = data['date_to'] or fields.Date.to_string(fields.Date.context_today(self))
        
        query = f"""
            SELECT
                ml.partner_id AS partner_id,
                SUM(CASE when ml.date < '{date_from}' Then ml.debit else 0 end) AS init_debit,
                SUM(CASE when ml.date < '{date_from}' Then ml.credit else 0 end) AS init_credit,
                SUM(CASE when ml.date < '{date_from}' Then ml.balance else 0 end) AS init_balance,
                SUM(CASE when ml.date >= '{date_from}' and ml.date <= '{date_to}' Then ml.balance else 0 end) AS balance,
                SUM(CASE when ml.date >= '{date_from}' and ml.date <= '{date_to}' Then ml.credit else 0 end)  AS credit,
                SUM(CASE when ml.date >= '{date_from}' and ml.date <= '{date_to}' Then ml.debit else 0 end)  AS debit
            from account_move_line ml
            join account_move move on move.id = ml.move_id
            join account_account account on account.id = ml.account_id
            {joins}
            {wheres}
            group by ml.partner_id"""
        self._cr.execute(query)
        return self._cr.dictfetchall()

    def get_detail_data(self, data, wheres, joins,lines):
        ''
        date_from = data['date_from'] or "2001-01-01"        
        date_to = data['date_to'] or fields.Date.to_string(fields.Date.context_today(self))
        
        total_list = {}

        wheres_date = f""
        wheres_date += f" and ml.date >= '{date_from}' and ml.date <= '{date_to}'"
 
        query = f"""
            SELECT
                ml.partner_id AS partner_id,
                (CASE when ml.date >= '{date_from}' and ml.date <= '{date_to}' Then ml.balance else 0 end) AS balance,
                (CASE when ml.date >= '{date_from}' and ml.date <= '{date_to}' Then ml.credit else 0 end)  AS credit,
                (CASE when ml.date >= '{date_from}' and ml.date <= '{date_to}' Then ml.debit else 0 end)  AS debit,
                move.name AS move_name,
                ml.date AS date,
                ml.name AS label
            from account_move_line ml
            join account_move move on move.id = ml.move_id
            join account_account account on account.id = ml.account_id
            join account_journal journal on journal.id = ml.journal_id
            {joins}
            {wheres + wheres_date}
            group by ml.partner_id,ml.id,ml.date,ml.debit,ml.credit,ml.balance,move.name,ml.date_maturity,ml.name
            ORDER BY ml.date ASC"""

        self._cr.execute(query)
        result = self._cr.dictfetchall()
        for line in result:
            if line['partner_id'] in total_list.keys():
                total_list[line['partner_id']] += [line]
            else:
                total_list.setdefault(line['partner_id'], [])
                total_list[line['partner_id']] += [line]

        return total_list
    


    def get_partner(self,partner_id):
        return self.env['res.partner'].browse(partner_id)

    @api.model
    def _get_report_values(self, docids, data=None):
        wheres = self.get_where(data, intial=False)
        joins = self.get_joins(data)
        lines = self.get_data(data, wheres, joins)
        detail_lines = {}
        if data['options'] == 'detailed':
            detail_lines = self.get_detail_data(data, wheres, joins,lines)
        
        account_name = ''
        if data['account_ids']:
            accounts = self.env['account.account'].browse(data['account_ids']) 
            for account in accounts:
                if account_name:
                    account_name += '/ ' + account.code + '' + account.name
                else:
                    account_name += account.code + '' + account.name
        data['account_name'] = account_name
        
        partner_tag_name = ''
        if data['partner_tag_ids']:
            tags = self.env['res.partner.category'].browse(data['partner_tag_ids']) 
            for tag in tags:
                if partner_tag_name:
                    partner_tag_name += '/ ' + tag.name
                else:
                    partner_tag_name += tag.name
        data['partner_tag_name'] = partner_tag_name
        
        return {
            'lines': lines,
            'detail_lines': detail_lines,
            'partner': self.get_partner,
            'data': data,
            'company': self.env.company,
            'lang': get_lang(self.env).code,
        }

class ReportPartnerLedgerDetails(models.AbstractModel):
    _name = 'report.partner_ledger_trial_balance.partnerledger_details'
    
    @api.model
    def _get_report_values(self, docids, data=None):
        result = self.env['report.partner_ledger_trial_balance.report_partnerledger']._get_report_values(self, data=data)

        return result

class PartnerLedgerXlsxReport(models.AbstractModel):
    _name = 'report.partner_ledger_trial_balance.partner_ledger_xlsx_report'
    _inherit = 'report.report_xlsx.abstract'
    _description = 'Payslip Batch XLSX Report'
    
    @api.model
    def generate_xlsx_report(self, workbook, data, objs):
        result = self.env['report.partner_ledger_trial_balance.report_partnerledger']._get_report_values(self, data=data)
        data = result['data']
        sheet = workbook.add_worksheet(_('Partner Account Statement'))
        lang = get_lang(self.env).code
        if lang == 'ar_001':
            sheet.right_to_left()
        if data['options'] == 'total':
            sheet.set_column('B:B', 15)
            sheet.set_column('C:C', 20)
            sheet.set_column('D:N', 15)
        if data['options'] == 'detailed':
            sheet.set_column('B:B', 15)
            sheet.set_column('C:D', 15)
            sheet.set_column('E:E', 20)
            sheet.set_column('F:N', 15)
        # if data['options'] == 'detailed':
        #     sheet.set_column('D:D', 20)
        sheet.set_default_row(25)

        format1 = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True,
            'font_size': 11,
            # 'indent': '2'
        })
        col_format1 = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True,
            'font_size': 11,
            # 'indent': '2'
        })
        format2 = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True,
            'bold': True,
            'font_size': 11,
        })
        format3 = workbook.add_format({
            'border': 1,
            'align': 'right' if lang == 'ar_001' else 'left',
            'valign': 'vcenter',
            'text_wrap': True,
            'bold': True,
            'font_size': 12,
        })
        format5 = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True,
            'bold': True,
            'bg_color': '#DCDCDC',
            'font_size': 12,
        })
        price_format1 = workbook.add_format({
            'border': 1,
            'align': 'right',
            'valign': 'vcenter',
            'text_wrap': True,
            'num_format': '#,##0.00',
            'font_size': 11,
        })
        price_format3 = workbook.add_format({
            'border': 1,
            'align': 'right',
            'valign': 'vcenter',
            'text_wrap': True,
            'bold': True,
            'num_format': '#,##0.00',
            'font_size': 11,
        })
        price_format2 = workbook.add_format({
            'border': 1,
            'align': 'right',
            'valign': 'vcenter',
            'text_wrap': True,
            'num_format': '#,##0.00',
            'bold': True,
            'font_size': 12,
        })
        total_price_format = workbook.add_format({
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True,
            'bold': True,
            'num_format': '#,##0.00',
            'bg_color': '#DCDCDC',
            'font_size': 12,
        })
        format2.set_align('center')

        col = 3
        if data['options'] == 'detailed':
            col = 2
        sheet.merge_range(1, col, 3, col+5, _("Partner Account Statement"), format5)

        # Filters
        col = 2
        if data['options'] == 'detailed':
            col = 1
        sheet.write(5, col, _('Date From'), format5)
        col += 1
        sheet.merge_range(5, col, 5, col+1,  data['date_from'], format2)
        col += 3
        sheet.merge_range(5, col, 5, col+1, _('Date To'), format5)
        col += 2
        sheet.merge_range(5, col, 5, col+1,  data['date_to'], format2)

        account = ''
        if data['result_selection'] == 'customer':
            account = _('Receivable Accounts')
        if data['result_selection'] == 'supplier':
            account = _('Payable Accounts')
        if data['result_selection'] == 'supplier':
            account = _('Receivable and Payable Accounts')
        
        col = 2
        if data['options'] == 'detailed':
            col = 1
        sheet.write(6, col, _('Accounts'), format5)
        col += 1
        sheet.merge_range(6, col, 6, col+1, data['account_ids'] and data['account_name'] or '-', format2)
        col += 3
        sheet.merge_range(6, col, 6, col+1, _("Account Type"), format5)
        col += 2
        sheet.merge_range(6, col, 6, col+1, account, format2)
        
        col = 2
        if data['options'] == 'detailed':
            col = 1
            
        sheet.write(7, col, _("Target Moves"), format5) 
        col += 1  
        sheet.merge_range(7, col, 7, col+1, (data['target_move'] == 'all' and _('All Entries')) or 
                    (data['target_move'] == 'posted' and _('All Posted Entries')), format2)
        col += 3
        sheet.merge_range(7, col, 7, col+1, _('Partner Tags'), format5)
        col += 2
        sheet.merge_range(7, col, 7, col+1, data['partner_tag_ids'] and data['partner_tag_name'] or '-', format2)
        

        row = 9
        col = 1
        if data['options'] == 'total':
            sheet.merge_range(row, col, row+1, col, _("Partner No"), format5)
            col += 1
            sheet.merge_range(row, col, row+1, col+1, _("Partner Name"), format5)
            col += 2
            sheet.merge_range(row, col, row, col+1, _("Opening Balance"), format5)
            col += 2
            sheet.merge_range(row, col, row, col+1, _("Transactions"), format5)
            col += 2
            sheet.merge_range(row, col, row, col+1, _("Ending Balance"), format5)
            
            
            row += 1
            col = 4
            sheet.write(row, col, _('Debit'), format5)
            col += 1
            sheet.write(row, col, _('Credit'), format5)
            col += 1
            sheet.write(row, col, _('Debit'), format5)
            col += 1
            sheet.write(row, col, _('Credit'), format5)
            col += 1
            sheet.write(row, col, _('Debit'), format5)
            col += 1
            sheet.write(row, col, _('Credit'), format5)
            col += 1
        else:
            sheet.write(row, col, _('Partner'), format5)
            col += 1
            sheet.write(row, col, _('Date'), format5)
            col += 1
            sheet.write(row, col, _('Entry'), format5)
            col += 1
            sheet.merge_range(row, col, row, col+1, _("Label"), format5)
            col += 2
            sheet.write(row, col, _('Debit'), format5)
            col += 1
            sheet.write(row, col, _('Credit'), format5)
            col += 1
            sheet.write(row, col, _('Balance'), format5)
            col += 1
        
        row += 1
        col = 1
        total_debit = total_credit = total_balance = total_balance1 = 0
        init_total_debit = init_total_credit = init_total_balance = 0
        lines = result['lines']
        detail_lines = result['detail_lines']
        for line in lines:

            if data['options'] == 'total':
                format = format1
                price_format = price_format1
            else:
                format = format3
                price_format = price_format2

            col = 1
            total_debit += line['debit']
            total_credit += line['credit']
            total_balance += line['balance'] + line['init_balance']
            init_debit = line['init_balance'] > 0 and line['init_balance'] or 0
            init_credit = line['init_balance'] < 0 and abs(line['init_balance']) or 0
            total_balance1 = line['init_balance']
            init_total_debit += init_debit
            init_total_credit += init_credit
            init_total_balance += line['init_balance']
            if not (line['init_balance'] == 0 and line['debit'] == 0 and line['credit'] == 0):
                partner_id = result['partner'](line['partner_id'])
                if data['options'] == 'total':
                    sheet.write(row, col, partner_id.ref or '', format)
                    col += 1
                    sheet.merge_range(row, col, row, col+1, (partner_id.name or _('Unkown Partner')), format)
                    col += 2
                
                    sheet.write(row, col, init_debit, price_format)
                    col += 1
                    sheet.write(row, col, init_credit, price_format)
                    col += 1
                    sheet.write(row, col, line['debit'], price_format)
                    col += 1
                    sheet.write(row, col, line['credit'], price_format)
                    col += 1
                    sheet.write(row, col,((line['init_balance'] + line['balance']) > 0 and (line['init_balance'] + line['balance']) or 0), price_format)
                    col += 1
                    sheet.write(row, col,((line['init_balance'] + line['balance']) < 0 and abs(line['init_balance'] + line['balance']) or 0), price_format)
                    col += 1
                else:
                    sheet.merge_range(row, col, row, col+7, (partner_id.ref or '') + ' ' + (partner_id.name or _('Unkown Partner')), format)
                    col += 5
                    # sheet.write(row, col, init_debit + line['debit'], price_format)
                    # col += 1
                    # sheet.write(row, col, init_credit + line['credit'], price_format)
                    # col += 1
                    # sheet.write(row, col, (total_balance1 or 0) + (line['balance'] or 0), price_format)
                    # col += 1
            row += 1
            count = 1
            if data['options'] == 'detailed':
                col = 1
                sheet.write(row, col, count, col_format1)
                col += 1
                sheet.write(row, col, '', col_format1)
                col += 1
                sheet.write(row, col, '', col_format1)
                col += 1
                sheet.merge_range(row, col, row, col+1, _('Initial Balance'), col_format1)
                col += 2
                sheet.write(row, col, init_debit, price_format1)
                col += 1
                sheet.write(row, col, init_credit, price_format1)
                col += 1
                sheet.write(row, col, total_balance1, price_format1)
                col += 1
                row += 1
                count += 1
                if line['partner_id'] in detail_lines.keys():
                    for sub_line in detail_lines[line['partner_id']]:
                        total_balance1 += sub_line['balance']
                        col = 1
                        sheet.write(row, col, count, col_format1)
                        col += 1
                        sheet.write(row, col, fields.Date.to_string(sub_line['date']), col_format1)
                        col += 1
                        sheet.write(row, col, sub_line['move_name'], col_format1)
                        col += 1
                        sheet.merge_range(row, col, row, col+1, sub_line['label'], col_format1)
                        col += 2
                        sheet.write(row, col, sub_line['debit'], price_format1)
                        col += 1
                        sheet.write(row, col, sub_line['credit'], price_format1)
                        col += 1
                        sheet.write(row, col, total_balance1, price_format1)
                        col += 1
                        row += 1
                        count += 1
                col = 1
                sheet.write(row, col, '#', format2)
                col += 1
                sheet.write(row, col, '', format2)
                col += 1
                sheet.write(row, col, '', format2)
                col += 1
                sheet.merge_range(row, col, row, col+1, _('Ending Balance'), format2)
                col += 2
                sheet.write(row, col, init_debit + line['debit'], price_format3)
                col += 1
                sheet.write(row, col, init_credit + line['credit'], price_format3)
                col += 1
                sheet.write(row, col, (line['init_balance'] or 0) + (line['balance'] or 0), price_format3)
                col += 1
                row += 1
                
        col = 1
        if data['options'] == 'total':
            sheet.merge_range(row, col, row, col+2, _("Total"), format5)
            col += 3

            sheet.write(row, col, init_total_debit, total_price_format)
            col += 1
            sheet.write(row, col, init_total_credit, total_price_format)
            col += 1
            sheet.write(row, col, total_debit, total_price_format)
            col += 1
            sheet.write(row, col, total_credit, total_price_format)
            col += 1
            sheet.write(row, col, (total_balance > 0 and total_balance or 0), total_price_format)
            col += 1
            sheet.write(row, col, (total_balance < 0 and abs(total_balance) or 0), total_price_format)
            col += 1
            
        if lines and len(lines) != 1 and data['options'] == 'detailed':
            sheet.merge_range(row, col, row, col+4, _("Total"), format5)
            col += 5
            sheet.write(row, col, (total_debit + init_total_debit), price_format)
            col += 1
            sheet.write(row, col, (total_credit + init_total_credit), price_format)
            col += 1
            sheet.write(row, col, total_balance, price_format)
            col += 1
            row += 1