# -*- coding: utf-8 -*-

from odoo import models, fields, api,fields, _
from dateutil.relativedelta import relativedelta

from odoo.exceptions import ValidationError

_states = {'draft': [('readonly', False)]}


def relativeDelta(enddate, startdate):
    if not startdate or not enddate:
        return relativedelta()
    startdate = fields.Datetime.from_string(startdate)
    enddate = fields.Datetime.from_string(enddate) + relativedelta(days=1)
    return relativedelta(enddate, startdate)


def delta_desc(delta):
    res = []
    if delta.years:
        res.append('%s Years' % delta.years)
    if delta.months:
        res.append('%s Months' % delta.months)
    if delta.days:
        res.append('%s Days' % delta.days)
    return ', '.join(res)


class EndOfService(models.Model):
    _name = 'hr.end_of_service'
    _description = 'End of Service'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, readonly=True, copy=False, default=_('New'))
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, states=_states,
                                  domain=[('contract_ids', '!=', False)])
    date = fields.Date('End of Service Date', required=True)

    department_id = fields.Many2one('hr.department', related='employee_id.department_id', readonly=True)
    job_id = fields.Many2one('hr.job', related='employee_id.job_id', readonly=True)
    manager_id = fields.Many2one('hr.employee', related='employee_id.parent_id', readonly=True)
    reason_id = fields.Many2one('hr.end_of_service.reason', string='End of Service Reason', required=True, )
    termination_reason_id = fields.Many2one('hr.end_of_service.termination_reason', string='Termination Reason')
    company_id = fields.Many2one('res.company', required=True, string='Company', default=lambda self: self.env.company)
    comments = fields.Text()
    join_date = fields.Date('Join Date', compute='_calc_join_date', store=True)
    service_year = fields.Float('Total Service Years', compute='_calc_service_year', store=True)
    service_month = fields.Float('Total Service Months', compute='_calc_service_year', store=True)
    service_desc = fields.Char('Total Service', compute='_calc_service_year', store=True)
    unpaid_leave_month = fields.Float('Unpaid Leave Months', compute='_calc_service_year', store=True)
    unpaid_leave_desc = fields.Char('Unpaid Leave', compute='_calc_service_year', store=True)
    payslip_id = fields.Many2one('hr.payslip', string='Pay Slip', ondelete='restrict')
    remaining_leaves = fields.Float('Remaining Leaves', compute='_calc_remaining_leaves')
    leave_compensation = fields.Float('Leaves Compensation', compute='_calc_remaining_leaves')
    amount = fields.Float(compute='_calc_amount', store=True)
    reward_amount = fields.Float(compute='_calc_reward_amount', store=True, string='Reward Amount')
    state = fields.Selection([('new', 'Draft'), ('confirm', 'Confirmed'),
                              ('approve', 'Approved'), ('refuse', 'Refused'),
                              ('cancel', 'Cancelled'), ('paid', 'Paid')], default='new', tracking=True)
    salary_compensation = fields.Float(string='Salary Compensation')
    balance = fields.Float('Balance')

    @api.onchange('employee_id')
    def _onchange_partner_id(self):
        # LEFT JOIN account_account_type at ON (acc.user_type_id=at.id)
        # AND at.id IN %s
        partner_id = self.employee_id.address_home_id
        if partner_id:
            z = [1, 2]
            date = fields.Date.today()
            params = [partner_id.id, str(date)]
            query = """
                SELECT  mv.state,"account_move_line".date,"account_move_line".id,"account_move_line".debit as debit, "account_move_line".credit as credit,"account_move_line".amount_currency as currency
                FROM account_move_line
                LEFT JOIN account_move mv ON ("account_move_line".move_id = mv.id)
                LEFT JOIN account_journal j ON ("account_move_line".journal_id = j.id)
                LEFT JOIN account_account acc ON ("account_move_line".account_id = acc.id)
                LEFT JOIN res_currency c ON ("account_move_line".currency_id=c.id)
                LEFT JOIN account_move m ON (m.id="account_move_line".move_id)
                WHERE 
                    "account_move_line".partner_id = %s
                    AND "account_move_line".date <= %s
                    AND mv.state = 'posted'
                    ORDER BY "account_move_line".date
                    """
            self.env.cr.execute(query, tuple(params))
            int = self.env.cr.dictfetchall()
            c = 0
            sum = 0
            for r in int:
                r['balance'] = r['debit'] - r['credit']
                sum += r['currency']
                c = c + r['balance']
                r['date'] = str(r['date'])
            self.balance = sum

    @api.constrains("employee_id", "state")
    def _check_duplication(self):
        for rec in self:
            if self.env['hr.end_of_service'].search([('id', '!=', rec.id), ('employee_id', '=', rec.employee_id.id),
                                                     ('state', 'not in', ('refuse', 'cancel'))]):
                raise ValidationError(_("You can't create more than one end of service per employee."))

    def action_confirm(self):
        self.state = 'confirm'

    def action_approve(self):
        self.state = 'approve'

    def action_reject(self):
        self.state = 'refuse'

    def action_draft(self):
        self.state = 'new'

    def action_cancel(self):
        self.state = 'cancel'

  
    def write(self, val):
        if 'state' in val and val.get('state') == 'paid':
            self.terminate_contract()
        res = super(EndOfService, self).write(val)
        return res
    
    def terminate_contract(self):
        self.employee_id.contract_id.state = 'close'
        self.employee_id.contract_id.active = False
        self.employee_id.active = False

    @api.depends('employee_id')
    def _calc_remaining_leaves(self):
        for rec in self:
            rec.remaining_leaves = 0
            rec.leave_compensation = 0
            if rec.employee_id:
                leave_balance = self.env['hr.leave.balance'].sudo().search([('employee_id', '=', rec.employee_id.id),
                                                                            ('leave_type', '=',
                                                                             rec.employee_id.contract_id.timeoff_type.id)])
                if leave_balance:
                    rec.remaining_leaves = leave_balance.remaining
                    rec.leave_compensation = (rec.employee_id.contract_id.wage / 30) * leave_balance.remaining

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id and self.employee_id.company_id != self.company_id:
            self.company_id = self.employee_id.company_id

    @api.model_create_multi
    @api.returns('self', lambda value: value.id)
    def create(self, vals_list):
        for vals in vals_list:
            vals['name'] = self.env['ir.sequence'].with_company(vals.get('company_id')).next_by_code(self._name)
        return super(EndOfService, self).create(vals_list)

    @api.depends('payslip_id.line_ids.amount')
    def _calc_amount(self):
        for record in self:
            record.amount = record.mapped('payslip_id.line_ids').filtered(lambda line: line.code == 'NET').amount

    @api.depends('reason_id', 'join_date', 'date', 'employee_id','reward_amount')
    def _calc_reward_amount(self):
        for record in self:
            contract_id = record.employee_id.contract_id
            record.reward_amount = self.reason_id.get_reward_amount(record.service_month, contract_id)

    @api.depends('employee_id.contract_ids.date_start')
    def _calc_join_date(self):
        for record in self:
            # Review
            # date_start = record.mapped('employee_id.contract_ids.date_start')
            date_start = record.mapped('employee_id.join_date')
            record.join_date = min(date_start) if date_start else False

    @api.depends('join_date', 'date', 'employee_id')
    def _calc_service_year(self):
        for record in self:
            unpaid_leave_delta = relativedelta()
            unpaid_leave_ids = self.env['hr.leave'].sudo().search([('employee_id', '=', record.employee_id.id),
                                                                   ('state', '=', 'validate'),
                                                                   ('holiday_status_id.unpaid', '=', True)])
            for leave_id in unpaid_leave_ids:
                unpaid_leave_delta += relativeDelta(leave_id.date_to, leave_id.date_from)

            delta = relativeDelta(record.date, record.join_date)
            record.service_desc = delta_desc(delta)

            if self.env['ir.config_parameter'].sudo().get_param('hr.end_of_service.unpaid_leave') == 'True':
                delta -= unpaid_leave_delta

            record.unpaid_leave_desc = delta_desc(unpaid_leave_delta)
            record.unpaid_leave_month = (unpaid_leave_delta.years * 12) + (unpaid_leave_delta.months) + (
                    unpaid_leave_delta.days / 30.0)

            service_month = (delta.years * 12) + (delta.months) + (delta.days / 30.0)
            service_year = service_month / 12.0
            record.service_year = service_year
            record.service_month = service_month

    def unlink(self):
        if any(self.filtered(lambda record: record.state != 'new')):
            raise ValidationError(_('You can delete draft status only'))
        return super(EndOfService, self).unlink()

    def _on_approve(self):
        if not self.payslip_id:
            raise ValidationError(_('No Pay Slip'))
        if not self.payslip_id.state != 'done':
            self.payslip_id.action_payslip_done()
        super(EndOfService, self)._on_approve()

    def action_payslip(self):
        if not self.payslip_id:
            date_from = fields.Date.from_string(self.date) + relativedelta(day=1)
            date_to = date_from + relativedelta(day=31)
            date_from = fields.Date.to_string(date_from)
            payslip = self.env['hr.payslip'].sudo().create({'employee_id': self.employee_id.id,
                                                            'date_from': date_from,
                                                            'date_to': date_to,
                                                            'name': 'Test',
                                                            'end_of_service_id': self.id})
            # Review
            # payslip.onchange_employee()
            payslip.compute_sheet()
            self.write({'payslip_id': payslip.id})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hr.payslip',
            'name': 'Pay slip',
            'res_id': self.payslip_id.id,
            'view_mode': 'form',
        }
