# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ReligionReligion(models.Model):
    _name = 'religion.religion'
    _description = 'Religion'

    name = fields.Char(string='Name', translate=True)
