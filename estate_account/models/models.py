# -*- coding: utf-8 -*-

from odoo import models, fields, api


class EstatePropertyInherited(models.Model):
    _inherit = 'real.estate'

    def property_sold(self):
        res = super(EstatePropertyInherited, self).property_sold()
        invoice_line = []
        invoice_line.append((0, 0, {
            'name': self.name,
            'quantity': 1.0,
            'price_unit': self.selling_price,
        }))
        invoice_line.append((0, 0, {
            'name': 'Property Sale (6%)',
            'quantity': 1.0,
            'price_unit': self.selling_price * 0.06,

        }))
        invoice_line.append((0, 0, {
            'name': 'Administrative Fees',
            'quantity': 1.0,
            'price_unit': 100.00,
        }))
        invoice_vals = {
            'partner_id': self.buyer_name,
            'move_type': 'out_invoice',
            'invoice_line_ids': invoice_line,
        }
        invoice = self.env['account.move'].create(invoice_vals)
        return invoice