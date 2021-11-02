# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import timedelta

class CrossoveredBudget(models.Model):
    _inherit = "crossovered.budget"

    restrict_allow = fields.Selection([('allow','Allow'),('restrict' , 'Restrict')],string="Allow/Restrict Override Amount",default="restrict")
    pertial = fields.Boolean(string='')

    analytic_id = fields.Many2one('account.analytic.account',string="Analytic Account")



    @api.onchange('date_to','date_from')
    def _onchange_date(self):
        if self.date_to and self.date_from:
            if self.date_from > self.date_to:
                raise ValidationError(_("Please select a proper date."))

    @api.model
    def default_get(self,fields):

        res = super(CrossoveredBudget,self).default_get(fields)
        vals = self.env['res.config.settings'].search([],limit=1,order="id desc")
        if vals.partial_budget_approve == True:
            res.update({'pertial':True})
        else:
            res.update({'pertial':False})
        return res

class CrossoveredBudgetLines(models.Model):
    _inherit = "crossovered.budget.lines"

    pertial_id = fields.Boolean(related='crossovered_budget_id.pertial')
    pertial_amount = fields.Float(string='Partial Amount')

    @api.onchange('date_to','date_from')
    def _onchange_date(self):
        if self.date_to and self.date_from:
            if self.date_from > self.date_to:
                raise ValidationError(_("Please select a proper date."))

    @api.model
    def create(self, vals):
        res = super(CrossoveredBudgetLines, self).create(vals)
        if res.crossovered_budget_id:
            res.write({'analytic_account_id':res.crossovered_budget_id.analytic_id.id})
        return res

    @api.depends('date_from', 'date_to')
    def _compute_theoritical_amount(self):
        today = fields.Date.today()
        for line in self:
            if line.paid_date:
                if today <= line.paid_date:
                    theo_amt = 0.00
                else:
                    if line.pertial_amount > 0:
                        theo_amt = line.pertial_amount
                    else:
                        theo_amt = line.planned_amount
            else:
                if not line.date_from or not line.date_to:
                    line.theoritical_amount = 0
                    continue

                line_timedelta = line.date_to - line.date_from + timedelta(days=1)
                elapsed_timedelta = today - line.date_from + timedelta(days=1)

                if elapsed_timedelta.days < 0:
                    theo_amt = 0.00
                elif line_timedelta.days > 0 and today < line.date_to:
                    if line.pertial_amount > 0:
                        theo_amt = (elapsed_timedelta.total_seconds() / line_timedelta.total_seconds()) * line.pertial_amount
                    else:
                        theo_amt = (elapsed_timedelta.total_seconds() / line_timedelta.total_seconds()) * line.planned_amount
                else:
                    if line.pertial_amount > 0:
                        theo_amt = line.pertial_amount
                    else:
                        theo_amt = line.planned_amount
            line.theoritical_amount = theo_amt