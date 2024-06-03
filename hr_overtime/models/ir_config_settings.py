from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    default_weekday_hour_rate = fields.Float(related='company_id.weekday_hour_rate', string='Weekday OT Hour Rate',
                                             readonly=0, deault=1.5, default_model="hr.overtime")
    default_weekend_hour_rate = fields.Float(related='company_id.weekend_hour_rate', string='Weekend OT Hour Rate',
                                             readonly=0, default=2.0, default_model="hr.overtime")
    default_holiday_hour_rate = fields.Float(related='company_id.holiday_hour_rate', string='Holiday OT Hour Rate',
                                             readonly=0, default=2.0, default_model="hr.overtime")
