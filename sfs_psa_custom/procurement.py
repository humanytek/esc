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

from osv import osv

class procurement_order(osv.osv):
    
    _inherit = "procurement.order"
    
    def create_procurement_purchase_order(self, cr, uid, procurement, po_vals, line_vals, context=None):
        """Add Brand to the Created purchase order from the procurement, using
           the provided field values, after adding the given purchase
           order line in the purchase order."""
        sale_line_pool = self.pool.get('sale.order.line')
        sale_order_line_id = sale_line_pool.search(cr, uid, 
                                                   [('procurement_id','=',procurement.id)],
                                                   context=context)[0]
        sale_order_line_rec = sale_line_pool.browse(cr, uid, sale_order_line_id, context=context)
        line_vals.update({'brand_id': sale_order_line_rec.brand_id.id or False})
        return super(procurement_order, self).create_procurement_purchase_order(cr, uid, procurement, po_vals, 
                                                                                line_vals, context=context)   

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: