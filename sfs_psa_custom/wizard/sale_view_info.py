# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2014 SF Soluciones.
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

from openerp.osv import osv, fields

class brand_stock_price(osv.osv_memory):
    
    _name = "brand.stock.price"
    _columns = {
                'brand': fields.many2one('product.brand', 'Brand'),
                'real_stock':  fields.float("Real Stock"),
                'unit_price': fields.float("Unit Price"),
                'view_button_id': fields.many2one("sale.order.line.view.info", "info_id")
                }
class sale_order_line_view_info(osv.osv_memory):
        
    _name = "sale.order.line.view.info"
    
    _columns = {
                'stock_price_ids' : fields.one2many('brand.stock.price', 'view_button_id', "Quantity and unit price Per Brand")
                }
    
    def default_get(self, cr, uid, fields, context=None):
        if context is None: context = {}
        context.update({
                        'states' : ['done'],
                        'what' : ('in','out')
                        })
        res = super(sale_order_line_view_info, self).default_get(cr, uid, fields, context=context)
        product = context.get('product_id', [])
        pricelist = context.get('pricelist', False)
        date_order = context.get('date_order', False)
        qty = context.get('quantity', False)
        uom = context.get('uom', False)
        product_pool = self.pool.get('product.product')
        product_rec = product_pool.browse(cr, uid, product, context=context)
        seller_recs = product_rec.seller_ids
        value_list = []
        for seller_rec in seller_recs:
            price = self.pool.get('product.pricelist').price_get(cr, uid, [pricelist],
                            product, qty or 1.0, seller_rec.name.id, {
                                'uom': uom,
                                'date': date_order,
                                })[pricelist]
            brand = seller_rec.brand_id and seller_rec.brand_id.id or False
            context.update({'brand' : [brand]})
            print product,'############################',context
            real_stock_per_brand = product_pool.get_product_available_per_brand(cr, uid, [product], context=context)
            value_list.append({
                               'brand': brand, 
                               'unit_price': price, 
                               'real_stock': real_stock_per_brand.values() and real_stock_per_brand.values()[0]}) 
        res['stock_price_ids'] = value_list
        return res
    
sale_order_line_view_info()
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
