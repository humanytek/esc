# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Humanytek (<http://humanytek.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import *
import logging
_logger = logging.getLogger(__name__)

class sale_order_line_esc(osv.Model):

    _inherit = 'sale.order.line'
    _description = 'Personalizacion para lineas de pedidos en ordenes de venta'
    
    # 15/12/2015 (felix) Metodo para capturar referencia del cliente
    def _get_client_ref(self, cr, uid, ids, field_name, args, context):
        res = {}
        for i in self.browse(cr, uid, ids, context):
            res[i.id] = ''
            if i.order_id.id:
                if i.order_id.client_order_ref:
                    res[i.id] = i.order_id.client_order_ref
        return res
        
    # 15/12/2015 (felix) Metodo para capturar divisa de la moneda
    def _get_divisa(self, cr, uid, ids, field_name, args, context):
        res = {}
        for i in self.browse(cr, uid, ids, context):
            res[i.id] = 0
            if i.order_id.id:
                if i.order_id.pricelist_id.id:
                    res[i.id] = i.order_id.pricelist_id.id
        return res
        
    # 15/12/2015 (felix) Metodo para capturar cant. entregada
    def _get_cant_entregada(self, cr, uid, ids, field_name, args, context):
        res = {}
        obj_stock_move = self.pool.get('stock.move')
        for i in self.browse(cr, uid, ids, context):
            res[i.id] = 0.000
            if i.order_id.id:
                src_stock_move = obj_stock_move.search(cr, uid, [('sale_line_id', '=', i.order_id.id), ('state', '=', 'done')])
                if src_stock_move:
                    for sm in obj_stock_move.browse(cr, uid, src_stock_move, context):
                        res[i.id] += sm.product_uos_qty
        return res
    
    _columns = {
        'client_order_ref': fields.function(_get_client_ref, type='char', 
            string='Ref. Cliente'),
        'divisa': fields.function(_get_divisa, type='many2one', obj='product.pricelist', 
            string='Divisa'),
        'cant_entregada': fields.function(_get_cant_entregada, type='float', 
            string='Cant. Entregada', digits=(10,3)),
    }
    
sale_order_line_esc()
