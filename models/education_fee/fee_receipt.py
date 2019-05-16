# -*- coding: utf-8 -*-

import datetime
from odoo import models, fields, api, _


class FeeReceipts(models.Model):
    _inherit = 'account.invoice'

    # mofify fields
    student_id = fields.Many2one('education.student', string='Student ID') # Admission No to Student ID

    # add fields
    # TODO: check duplacated invoice with A.Y when create
    application_id = fields.Many2one('education.application', string='Application No',  
        default=lambda self: self.env.context.get('active_id'),
        domain="[('state', '=', 'verification')]")
    is_application_fee = fields.Boolean(string='Is Application Fee', store=True, default=False)
    
    @api.onchange('student_id', 'fee_category_id', 'payed_from_date', 'payed_to_date', 'application_id')
    def _get_partner_details(self):
        """Student_id is inherited from res_partner. Set partner_id from student_id """
        self.ensure_one()
        lines = []
        for item in self:
            item.invoice_line_ids = lines
            if item.application_id:
                item.partner_id = item.application_id.partner_id
                item.student_name = item.application_id.partner_id.name
            else:
                item.partner_id = item.student_id.partner_id
            item.class_division_id = item.student_id.class_id
            date_today = datetime.date.today()
            company = self.env.user.company_id
            from_date = item.payed_from_date
            to_date = item.payed_to_date
            if not from_date:
                from_date = company.compute_fiscalyear_dates(date_today)['date_from']
            if not to_date:
                to_date = date_today
            if item.partner_id and item.fee_category_id:
                invoice_ids = self.env['account.invoice'].search([('partner_id', '=', item.partner_id.id),
                                                                  ('date_invoice', '>=', from_date),
                                                                  ('date_invoice', '<=', to_date),
                                                                  ('fee_category_id', '=', item.fee_category_id.id)])
                invoice_line_list = []
                for invoice in invoice_ids:
                    for line in invoice.invoice_line_ids:
                        fee_line = {
                            'price_unit': line.price_unit,
                            'quantity': line.quantity,
                            'product_id': line.product_id,
                            'price_subtotal': line.price_subtotal,
                            'invoice_line_tax_ids': line.invoice_line_tax_ids,
                            'discount': line.discount,
                            'date': line.invoice_id.date_invoice,
                            'receipt_no': line.invoice_id.number
                        }
                        invoice_line_list.append((0, 0, fee_line))
                item.payed_line_ids = invoice_line_list

    @api.model
    def create(self, vals):
        """ Adding two field to invoice. is_fee use to display fee items only in fee tree view"""
        partner_id = self.env['res.partner'].browse(vals['partner_id'])
        if 'fee_category_id' in vals:
            vals.update({
                'is_fee': True,
                'student_name': partner_id.name
            })
        if 'application_id' in vals:
            vals['is_application_fee'] = True
        res = super(FeeReceipts, self).create(vals)
        return res