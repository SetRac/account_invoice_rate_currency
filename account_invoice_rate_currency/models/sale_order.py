# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError
from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    rate_pricelist = fields.Char(string='RATE PRICELIST', help='Actualiza el precio segun este Valor siempre y cuando el Producto este en Dolares')
    total_pesos = fields.Float(string='TOTAL PESOS' )

    @api.onchange('rate_pricelist', 'amount_total')
    def button_update_prices_from_pricelist(self):
        try:
            rate_pricelist = float(self.rate_pricelist)
        except:
            message =  _(' La tasa debe ser un entero o Flotante')
            raise UserError(_(message))
        if self.amount_total != 0 and rate_pricelist  != False :
            self.total_pesos =  rate_pricelist * self.amount_total 
            
            
