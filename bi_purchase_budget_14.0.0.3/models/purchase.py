# -*- coding: utf-8 -*-
# Part of Browseinfo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _

from odoo.exceptions import ValidationError

class purchase_order_inherit(models.Model):
    _inherit = "purchase.order"

    analytic_account_id = fields.Many2one('account.analytic.account',string="Analytic Account")

    
    def button_confirm(self, force=False):


        if not self.analytic_account_id :
            res = super(purchase_order_inherit, self).button_confirm()
            return res

        else :
            budget_line = self.env['crossovered.budget.lines'].sudo().search([('date_from','<=',self.date_order),
                                                                            ('date_to','>=',self.date_order),
                                                                            ('analytic_account_id','=',self.analytic_account_id.id),
                                                                            ('company_id','=',self.company_id.id)])

            amount = self.currency_id._convert(self.amount_untaxed, self.company_id.currency_id, self.company_id, self.date_order.date() or fields.Date.today())
            planned_amount = 0.0
            practical_amount = 0.0
            for line in budget_line:
                planned_amount += line.planned_amount
                practical_amount += line.practical_amount
                
            for budget in budget_line:
                if budget and budget.crossovered_budget_id.state not in ['draft','done','cancel']:
                        if  planned_amount < abs(practical_amount) + amount :
                             if budget.crossovered_budget_id.restrict_allow == 'restrict' :
                            
                                raise ValidationError(
                                                 _("Don't have enough available amount for %s .")%self.analytic_account_id.name)
                            
        return super(purchase_order_inherit, self).button_confirm()

class PurchaseOrderLine_inherit(models.Model):
    _inherit = "purchase.order.line"

    account_analytic_id = fields.Many2one('account.analytic.account',string="Analytic Account",related="order_id.analytic_account_id",store=True)
    
class AccountInvoice_Inherit(models.Model):
    _inherit = "account.move"


    @api.model_create_multi
    def create(self, vals_list):
        # OVERRIDE
        
        moves = super(AccountInvoice_Inherit, self).create(vals_list)

        for move in moves:
            if move.reversed_entry_id:
                continue
            purchase = move.line_ids.mapped('purchase_line_id.order_id')
            
            if not purchase:
                continue

            else : 
                
                move.invoice_origin = purchase.name
            
        return moves


    def action_post(self):
        for moves in self:
            if moves.move_type == 'in_invoice' :
                analytic_budget = {}
                for line in moves.invoice_line_ids :
                    if line.analytic_account_id.id not in analytic_budget :
                        analytic_budget[line.analytic_account_id.id] = line.price_subtotal
                    else :
                        analytic_budget[line.analytic_account_id.id] = analytic_budget[line.analytic_account_id.id] + line.price_subtotal
                for account in analytic_budget :
                    if account :
                        date_check = fields.Date.today()
                        if moves.invoice_date :
                            date_check = moves.invoice_date    
                        budget_line = moves.env['crossovered.budget.lines'].sudo().search([('date_from','<=',date_check),
                                                                                ('date_to','>=',date_check),
                                                                                ('analytic_account_id','=',account)
                                                                                ])
                        amount = moves.currency_id._convert(analytic_budget[account], moves.company_id.currency_id, moves.company_id, date_check)
                        planned_amount = 0.0
                        practical_amount = 0.0
                        for line in budget_line:
                            planned_amount += line.planned_amount
                            practical_amount += line.practical_amount
                            
                        for budget in budget_line:
                            if budget and budget.crossovered_budget_id.state not in ['draft','done','cancel']:
                                    if  planned_amount < abs(practical_amount) + amount :
                                         if budget.crossovered_budget_id.restrict_allow == 'restrict' :
                                        
                                            raise ValidationError(
                                                             _("Don't have enough available amount for %s .")%line.analytic_account_id.name)

        res = super(AccountInvoice_Inherit, self).action_post()
        return res
