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

from osv import osv, fields

from openerp import tools
import openerp.addons.decimal_precision as dp

class stock_product_location(osv.osv):
    _name = 'stock.product.location'
    _description = 'Report to get stock of product based on location'
    _auto = False
    
    def _product_value(self, cr, uid, ids, field_names, arg, context=None):
        res = {}
        product_pool = self.pool.get('product.product')
        for obj in self.browse(cr, uid, ids, context=context):
            res[obj.id] = {
                           'stock_real': 0.00,
                           'stock_forcast': 0.00
                           }
            location_id = obj.location_id and obj.location_id.id or False
            product_id = obj.product_id and obj.product_id.id or False
            if location_id and product_id:
                ctx = context.copy()
                ctx['location'] = location_id
                product_obj = product_pool.browse(cr, uid, product_id, context=ctx)
                res[obj.id]['stock_real'] = product_obj.qty_available
                res[obj.id]['stock_forcast'] = product_obj.virtual_available
        return res
    
    _columns = {
                'name': fields.char('Product Reference', size=128),
                'product_id': fields.many2one('product.product', 'Product Name'),
                'location_id': fields.many2one('stock.location', 'Location Name'),
                'serial_number': fields.many2one('stock.production.lot', 'Serial No'),
                'stock_real': fields.function(_product_value, type='float', string='Real Stock', multi="stock"),
                'stock_forcast': fields.function(_product_value, type='float', string='Forecasted Stock', multi="stock"),
                'brand_id': fields.many2one('product.brand', 'Brand')
                }
    
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'stock_product_location')
        cr.execute("""create or replace view stock_product_location as (SELECT
                        CAST(CAST(x.product_id AS text)||CAST(x.location_id AS text) AS numeric(24,0)) as id,
                        pp.default_code AS name,
                        x.product_id as product_id,
                        x.location_id as location_id,
                        x.prodlot_id as serial_number,
                        x.brand_id as brand_id
                    FROM
                        (SELECT
                            DISTINCT product_id,
                            location_id,
                            prodlot_id,
                            brand_id
                        FROM
                            stock_move
                        UNION
                        SELECT
                            DISTINCT product_id,
                            location_dest_id as location_id,
                            prodlot_id,
                            brand_id
                        FROM stock_move) x
                    LEFT JOIN product_product pp ON pp.id = x.product_id
                    LEFT JOIN stock_location sl on sl.id = x.location_id
                    WHERE sl.usage = 'internal'
                    GROUP BY
                        pp.default_code,
                        x.product_id,
                        x.location_id,
                        x.prodlot_id,
                        x.brand_id)"""
                    )
stock_product_location()