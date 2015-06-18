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

from osv import fields, osv

class purchase_order(osv.osv):
    
    _inherit = 'purchase.order'
    
    def _prepare_order_line_move(self, cr, uid, order, order_line, picking_id, context=None):
        """Adds brand to the created stock move on confirming the purchase order"""
        res = super(purchase_order, self)._prepare_order_line_move(cr, uid, order, order_line, picking_id, context)
        res.update({'brand_id': order_line.brand_id and order_line.brand_id.id or False})
        print "_prepare_order_line_move","6"*90
        return res
    
purchase_order()

class purchase_order_line(osv.osv):
    
    _inherit = "purchase.order.line"
    _columns = {
                'brand_id': fields.many2one('product.brand','Brand')
                }
    
purchase_order_line()
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: