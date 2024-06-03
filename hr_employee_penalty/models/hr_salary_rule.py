from odoo import fields, models, api, _


class SalaryRule(models.Model):
    _inherit = "hr.salary.rule"

    struct_id = fields.Many2one('hr.payroll.structure', string='Salary Structure')
