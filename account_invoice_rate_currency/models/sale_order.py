# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, _
from odoo.exceptions import UserError, Warning, ValidationError
from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    rate_pricelist = fields.Char(string='RATE PRICELIST', help='Actualiza el precio segun este Valor siempre y cuando el Producto este en Dolares')
    total_pesos = fields.Float(string='TOTAL PESOS' )

    
         
    @api.multi
    def action_confirm(self, context=None):
        #print("REVISANDO LINEAS: ", self.order_line)
        
        try:
            rate_pricelist = float(self.rate_pricelist)
            
        except:
            message =  _(' La tasa debe ser un entero o Flotante')
            raise UserError(_(message))
        if self.amount_total != 0 and rate_pricelist  > 0 :
            #self.update_total_pesos()
            self.total_pesos =  rate_pricelist * self.amount_total
            return super(SaleOrder,self).action_confirm()   

                
        else:
                return super(SaleOrder,self).action_confirm()   

    @api.multi
    def update_total_pesos(self):
        try:
            rate_pricelist = float(self.rate_pricelist)
        except:
            message =  _(' La tasa debe ser un entero o Flotante')
            raise UserError(_(message))
        if self.amount_total != 0 and rate_pricelist  > 0 :
            self.total_pesos =  rate_pricelist * self.amount_total 
            
            
