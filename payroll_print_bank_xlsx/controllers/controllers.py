# -*- coding: utf-8 -*-
# from odoo import http


# class PayrollPrintBankXlsx(http.Controller):
#     @http.route('/payroll_print_bank_xlsx/payroll_print_bank_xlsx', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/payroll_print_bank_xlsx/payroll_print_bank_xlsx/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('payroll_print_bank_xlsx.listing', {
#             'root': '/payroll_print_bank_xlsx/payroll_print_bank_xlsx',
#             'objects': http.request.env['payroll_print_bank_xlsx.payroll_print_bank_xlsx'].search([]),
#         })

#     @http.route('/payroll_print_bank_xlsx/payroll_print_bank_xlsx/objects/<model("payroll_print_bank_xlsx.payroll_print_bank_xlsx"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('payroll_print_bank_xlsx.object', {
#             'object': obj
#         })
