from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    # address_home_id = fields.Many2one(
    #     'res.partner', 'Address',
    #     help='Enter here the private address of the employee, not the one linked to your company.',
    #     groups="hr.group_hr_user", tracking=True,
    #     domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
