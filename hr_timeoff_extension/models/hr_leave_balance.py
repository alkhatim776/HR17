# -*- coding: utf-8 -*-

from odoo import models, fields


class HrLeaveBalance(models.Model):
    _name = "hr.leave.balance"

    employee_no = fields.Char('Employee No', related="employee_id.employee_no")
    employee_id = fields.Many2one('hr.employee', 'Employee')
    leave_type = fields.Many2one('hr.leave.type', 'Leave Type', domain="[('is_annual', '=', True)]")
    balance = fields.Float('Balance', compute='_compute_total_balance')
    taken = fields.Float('Taken', compute='_compute_total_balance')
    remaining = fields.Float('Remaining', compute='_compute_total_balance')
    _rec_name = 'employee_id'

    def _compute_total_balance(self):
        for rec in self:
            balance = 0
            taken = 0
            if rec.employee_id and rec.leave_type:
                allocation = self.env['hr.leave.allocation'].sudo().search(
                    [('employee_id', '=', rec.employee_id.id), ('holiday_status_id', '=', rec.leave_type.id), ('state', '=', 'validate')])
                taken_leaves = self.env['hr.leave'].sudo().search(
                    [('employee_id', '=', rec.employee_id.id), ('holiday_status_id', '=', rec.leave_type.id),
                     ('state', '=', 'validate')])
                for line in  allocation:
                    balance += line.number_of_days_display

                for line in taken_leaves:
                    taken += line.number_of_days
            rec.balance = balance
            rec.taken = taken
            rec.remaining = balance - taken
            

