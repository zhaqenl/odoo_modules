# -*- coding: utf-8 -*-
"""Model file for sales inherit module
"""

from openerp import models, fields, api
# from logging import getLogger
# _log = logging.getLogger(__name__)


class SaleDiscount(models.Model):
    """Model containing discount-related fields for Sale
    """
    _inherit = "sale.order"
    discount_type = fields.Selection([('none', 'None'),
                                      ('rate', 'Rate'),
                                      ('fixed', 'Fixed')],
                                     "Discount Type",
                                     default='none')
    discount_rate = fields.Float("Discount Rate")
    fixed_amount = fields.Float("Fixed Amount")

    @api.onchange("discount_type", "discount_rate", "fixed_amount")
    def _compute_discount(self):
        for rec in self:
            line_amount = len(rec.order_line)

        for rec in self.order_line:
            d_type = self.discount_type
            if d_type == "fixed":
                rec.discount = ((self.fixed_amount / line_amount)
                                / (rec.price_unit * rec.product_uom_qty) * 100)
            elif d_type == "rate":
                rec.discount = self.discount_rate
            else:
                rec.discount = 0.00


class InvoiceDiscount(models.Model):
    """Model containing discount-related fields for Invoice
    """
    _inherit = "account.invoice"
    discount_type = fields.Selection([('none', 'None'),
                                      ('rate', 'Rate'),
                                      ('fixed', 'Fixed')],
                                     "Discount Type",
                                     default=(lambda self:
                                              self.env['sale.order'].search([]).
                                              discount_type))
    discount_rate = fields.Float("Discount Rate",
                                 default=(lambda self:
                                          self.env['sale.order'].search([]).
                                          discount_rate))
    fixed_amount = fields.Float("Fixed Amount",
                                default=(lambda self:
                                         self.env['sale.order'].search([]).
                                         fixed_amount))

    @api.onchange("discount_type", "discount_rate", "fixed_amount")
    def _compute_discount(self):
        for rec in self:
            line_amount = len(rec.invoice_line)

        for rec in self.invoice_line:
            d_type = self.discount_type
            if d_type == "fixed":
                rec.discount = ((self.fixed_amount / line_amount)
                                / (rec.price_unit * rec.quantity) * 100)
            elif d_type == "rate":
                rec.discount = self.discount_rate
            else:
                rec.discount = 0.00
