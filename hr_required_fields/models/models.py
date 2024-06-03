# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class hr_required_fields(models.Model):
#     _name = 'hr_required_fields.hr_required_fields'
#     _description = 'hr_required_fields.hr_required_fields'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
