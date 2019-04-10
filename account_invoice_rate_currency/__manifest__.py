# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'RATE Pricelist on Invoices',
    'version': '11.0.1.0.0',
    'summary': 'Add partner pricelist on invoices',
    'category': 'Accounting & Finance',
    'author': 'CACB,'
              'Cesar Chirinos,'
              'ConsulNET,'
              'Odoo Community Association (OCA)',
    'website': 'http://consulnet.cl',
    'license': 'AGPL-3',
    'depends': [
        'account','sale',
    ],
    'data': [
        'views/account_invoice_view.xml',
        'views/sale_order_view.xml',
    ],
    'demo': [
        'demo/res_groups.yml',
    ],
    'installable': True,
}
