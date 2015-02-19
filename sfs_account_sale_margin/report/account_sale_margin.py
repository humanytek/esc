# -*- encoding: utf-8 -*
##############################################################################
#
#    Copyright (c) 2013 SF Soluciones.
#    (http://www.sfsoluciones.com)
#    contacto@sfsoluciones.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import tools
import time 
from osv import fields,osv
import openerp.addons.decimal_precision as dp

class sale_margin_product(osv.osv):
    _name = "sale.margin_product"
    _description = "Sale Margin"
    _auto = False
    _rec_name = 'invoice_number'
    _columns = {
                'invoice_number': fields.char("Invoice number", size=64, readonly=True),
                'date_invoice': fields.date("Invoice date", readonly=True),
                'partner_id': fields.many2one('res.partner','Customer', readonly=True),
                'user_id': fields.many2one('res.users','Salesperson', readonly=True),
                'categ_id': fields.many2one('product.category','Product Category', readonly=True),
                'product_name': fields.char("Product name", size=128, readonly=True),
                'product_id' : fields.many2one("product.product", "Product"),
                'account_journal_id' : fields.many2one("account.journal", "Account Journal"),
                'quantity': fields.float("Quantity", readonly=True, digits_compute= dp.get_precision('Product UoS')),
                'uom': fields.many2one('product.uom','Unit of Measure', readonly=True),
                'price_unit': fields.float('Unit Price', readonly=True, digits_compute= dp.get_precision('Product Price'),
                                           group_operator="avg"),
                'standard_price': fields.float('Unit Cost', readonly=True, digits_compute= dp.get_precision('Product Price'),
                                               group_operator="avg"),
                'price_subtotal': fields.float('Product Amount', readonly=True, digits_compute= dp.get_precision('Account')),
                'cost_ammount': fields.float('Cost Amount', readonly=True, digits_compute= dp.get_precision('Account')),
                'margin': fields.float('Margin', readonly=True, digits_compute= dp.get_precision('Account')),
                'margin_percent': fields.char('Margin Percent', readonly=True)
                }
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'sale_margin_product')
        
        cr.execute("""
                   create or replace view sale_margin_product as (
                      select
                           y.id as id,
                           y.invoice_number as invoice_number,
                           y.date_invoice as date_invoice,
                           y.partner_id as partner_id,
                           y.user_id as user_id,
                           y.categ_id as categ_id,
                           y.product_name as product_name,
                           y.product_id as product_id,
                           y.account_journal_id as account_journal_id,
                           y.uom as uom,
                           y.price_unit as price_unit,
                           y.standard_price as standard_price,
                           y.quantity as quantity,
                           y.cost_ammount as cost_ammount,
                           y.price_subtotal as price_subtotal,
                           y.margin as margin,
                           case y.price_subtotal
                               when 0.00 Then 0.00 || '%'
                               else round((y.margin / y.price_subtotal),2) || '%'
                           END as margin_percent
                      from
                       (select 
                           x.id as id,
                           x.invoice_number as invoice_number,
                           x.date_invoice as date_invoice,
                           x.partner_id as partner_id,
                           x.user_id as user_id,
                           x.categ_id as categ_id,
                           x.product_name as product_name,
                           x.product_id as product_id,
                           x.account_journal_id as account_journal_id,
                           x.uom as uom,
                           x.price_unit as price_unit,
                           x.standard_price as standard_price,
                           x.quantity as quantity,
                           x.cost_ammount * x.quantity as cost_ammount,
                           x.price_subtotal * x.quantity as price_subtotal,
                           (x.price_subtotal * x.quantity - x.cost_ammount * x.quantity) as margin
                       from    
                         (select
                           min(ail.id) as id,
                           ai.number as invoice_number,
                           ai.date_invoice as date_invoice,
                           ai.partner_id as partner_id,
                           ai.user_id as user_id,
                           pt.categ_id as categ_id,
                           pt.name || pr.default_code as product_name,
                           ail.product_id as product_id,
                           ai.journal_id as account_journal_id,
                           ail.uos_id as uom,
                           ail.price_unit as price_unit,
                           pt.standard_price as standard_price,
                           case aj.type
                               When 'sale' Then sum(ail.quantity)
                               When 'sale_refund' Then -sum(ail.quantity)
                               else 0.00
                           End as quantity,
                           case aj.type
                               When 'sale' Then  (case 
                                                      when avg(pt.standard_price) ISNULL then 0.00
                                                      else avg(pt.standard_price) end)
                               When 'sale_refund' Then  (case
                                                      when avg(pt.standard_price) ISNULL then 0.00
                                                      else -avg(pt.standard_price) end)
                           End as cost_ammount,
                           case aj.type
                               When 'sale' Then (case 
                                                     when avg(ail.price_unit) ISNULL then 0.00
                                                     else avg(ail.price_unit) end)
                               When 'sale_refund' Then (case 
                                                          when avg(ail.price_unit) ISNULL then 0.00
                                                          else -avg(ail.price_unit) end)
                               else 0.00
                           End as price_subtotal
                        from account_invoice_line as ail
                           left join account_invoice ai on (ai.id = ail.invoice_id)
                           left join stock_move stm on (ail.stm_id = stm.id)
                           Left Join account_journal aj on (aj.id = ai.journal_id)
                           left join product_product pr on (pr.id=ail.product_id)
                           left join product_template pt on (pr.product_tmpl_id=pt.id)
                        where ai.type in ('out_invoice','out_refund')
                         and ai.state in ('open','paid')
                        group by
                           ai.number,
                           ai.date_invoice,
                           ai.partner_id,
                           ai.user_id,
                           pt.categ_id,
                           ai.journal_id,
                           pt.name,
                           pr.default_code,
                           ail.uos_id,
                           ail.price_unit,
                           ail.product_id,
                           pt.standard_price,
                           aj.type)x)y
                           );
                   """)

sale_margin_product()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:-