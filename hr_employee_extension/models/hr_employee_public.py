# -*- coding: utf-8 -*-

from odoo import models, fields


class HREmployee (models.Model):
    _inherit = 'hr.employee.public'
        
    employee_no = fields.Char(string='Employee Company ID', readonly=True) 
