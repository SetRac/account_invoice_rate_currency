# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError
from odoo import models, fields

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    rate_pricelist = fields.Char(string='RATE PRICELIST', help='Actualiza el precio segun este Valor siempre y cuando el Producto este en Dolares')
    pricelist_id = fields.Many2one(
        comodel_name='product.pricelist', string='Pricelist',
        readonly=True,
        states={'draft': [('readonly', False)]},
    )

    @api.multi
    def button_update_prices_from_pricelist(self):
        for inv in self.filtered(lambda r: r.state == 'draft'):
            inv.invoice_line_ids.filtered('product_id').update_from_pricelist()

class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'
    @api.onchange('product_id', 'quantity', 'uom_id')
    def _onchange_product_id_account_invoice_pricelist(self):
        class_sale_order = self.env['sale.order']
        name_sale_order = self.origin
        if not self.invoice_id.pricelist_id or not self.invoice_id.partner_id:
            return
        else:
            product = self.product_id.with_context(
                lang=self.invoice_id.partner_id.lang,
                partner=self.invoice_id.partner_id.id,  
                quantity=self.quantity,
                date_order=self.invoice_id.date_invoice,
                pricelist=self.invoice_id.pricelist_id.id,
                uom=self.uom_id.id,
                fiscal_position=(
                    self.invoice_id.partner_id.property_account_position_id.id)
                )
            if self.origin:
                order_sale = class_sale_order.search([('name', '=', name_sale_order)])
                if len(order_sale) > 0:
                    currency_sale= order_sale.pricelist_id.currency_id.name
                else:
                    currency_sale = False
            else:
                currency_sale = False
            rate = self.invoice_id.rate_pricelist
            if (  currency_sale == "USD" ) and  ( self.invoice_id.rate_pricelist != False )  :
                rate = rate.replace(",", ".")
                rate = float(rate)
                try:
                    self.price_unit = self.env['account.tax']._fix_tax_included_price(
                            float(self.price_unit) * float(rate) , product.taxes_id, self.invoice_line_tax_ids)
                except:
                    message =  ('Solo se admiten Numeros y Decimales en La Tasa de Cambio')
                    raise UserError(_(message))
                #raise ValidationError(_('La Tasa de Cambio ha modificado los Precios !'))
            else:
                self.price_unit = self.env['account.tax']._fix_tax_included_price(
                            product.price, product.taxes_id, self.invoice_line_tax_ids)


        
