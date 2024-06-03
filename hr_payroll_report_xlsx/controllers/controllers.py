# -*- coding: utf-8 -*-
# from odoo import http


# class HrPayrollReportXlsx(http.Controller):
#     @http.route('/hr_payroll_report_xlsx/hr_payroll_report_xlsx', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hr_payroll_report_xlsx/hr_payroll_report_xlsx/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('hr_payroll_report_xlsx.listing', {
#             'root': '/hr_payroll_report_xlsx/hr_payroll_report_xlsx',
#             'objects': http.request.env['hr_payroll_report_xlsx.hr_payroll_report_xlsx'].search([]),
#         })

#     @http.route('/hr_payroll_report_xlsx/hr_payroll_report_xlsx/objects/<model("hr_payroll_report_xlsx.hr_payroll_report_xlsx"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hr_payroll_report_xlsx.object', {
#             'object': obj
#         })
