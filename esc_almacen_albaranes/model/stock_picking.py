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
import logging
_logger = logging.getLogger(__name__)

class stock_picking_esc(osv.Model):

    _inherit = 'stock.picking'
    _description = 'Cambios en campos y modelos para Stock Picking'
    
    # 17/06/2015 (felix) Metodo para asignar valor a la operacion
    def _get_operacion(self, cr, uid, ids, fields_name, args, context=None):
        res = {}
        obj_sale_order = self.pool.get('sale.order')
        obj_purchase_order = self.pool.get('purchase.order')
        for i in self.browse(cr, uid, ids, context):
            res[i.id] = ''
            
            # Albaran de salida, captura una venta
            if i.origin and i.type in ['out']:
                src_sale_order = obj_sale_order.search(cr, uid, [('name', 'like', i.origin)])
                res[i.id] = obj_sale_order.browse(cr, uid, src_sale_order[0], context)['operaciones']
                
            # Albaran de entrada, captura una compra
            if i.origin and i.type in ['in']:
                doc = i.origin.split(':')
                if doc:
                    src_purchase_order = obj_purchase_order.search(cr, uid, [('name', 'like', doc[0])])
                else:
                    src_purchase_order = obj_purchase_order.search(cr, uid, [('name', 'like', i.origin)])
                res[i.id] = obj_purchase_order.browse(cr, uid, src_purchase_order[0], context)['operaciones']
            
        return res
    
    _columns = {
        'pedimento_id': fields.many2one('import.info', 'Pedimento'),
        'perfiles_ids': fields.related('partner_id', 'answers_ids', 
            type='many2many', relation='crm_profiling.answer', 
            string='Perfiles'),
        'preentrada_id': fields.many2one('stock.picking.pre', 
            'Codigo de pre-entrada'),
        'cliente_ref': fields.char('Referencia cliente', size=1024),
        'efectua_id': fields.many2one('res.users', 'Efectua'),
        'operaciones': fields.function(_get_operacion, type='selection', 
            selection=[('linea','Operaciones de linea'), 
            ('desarrollo','Operaciones de desarrollo')], string='Operacion')
    }
    
stock_picking_esc()


class stock_picking_in_esc(osv.Model):

    _inherit = 'stock.picking.in'
    _description = 'Cambios en campos y modelos para Stock Picking In'
    
    # 17/06/2015 (felix) Metodo para asignar valor a la operacion
    def _get_operacion(self, cr, uid, ids, fields_name, args, context=None):
        res = {}
        obj_sale_order = self.pool.get('sale.order')
        obj_purchase_order = self.pool.get('purchase.order')
        for i in self.browse(cr, uid, ids, context):
            res[i.id] = ''
            
            # Albaran de salida, captura una venta
            if i.origin and i.type in ['out']:
                src_sale_order = obj_sale_order.search(cr, uid, [('name', 'like', i.origin)])
                res[i.id] = obj_sale_order.browse(cr, uid, src_sale_order[0], context)['operaciones']
                
            # Albaran de entrada, captura una compra
            if i.origin and i.type in ['in']:
                doc = i.origin.split(':')
                if doc:
                    src_purchase_order = obj_purchase_order.search(cr, uid, [('name', 'like', doc[0])])
                else:
                    src_purchase_order = obj_purchase_order.search(cr, uid, [('name', 'like', i.origin)])
                res[i.id] = obj_purchase_order.browse(cr, uid, src_purchase_order[0], context)['operaciones']
            
        return res
    
    _columns = {
        'pedimento_id': fields.many2one('import.info', 'Pedimento'),
        'preentrada_id': fields.many2one('stock.picking.pre', 
            'Codigo de pre-entrada'),
        'operaciones': fields.function(_get_operacion, type='selection', 
            selection=[('linea','Operaciones de linea'), 
            ('desarrollo','Operaciones de desarrollo')], string='Operacion')
    }
    
stock_picking_in_esc()


class stock_picking_out_esc(osv.Model):

    _inherit = 'stock.picking.out'
    _description = 'Cambios en campos y modelos para Stock Picking Out'
    
    # 17/06/2015 (felix) Metodo para asignar valor a la operacion
    def _get_operacion(self, cr, uid, ids, fields_name, args, context=None):
        res = {}
        obj_sale_order = self.pool.get('sale.order')
        obj_purchase_order = self.pool.get('purchase.order')
        for i in self.browse(cr, uid, ids, context):
            res[i.id] = ''
            
            # Albaran de salida, captura una venta
            if i.origin and i.type in ['out']:
                src_sale_order = obj_sale_order.search(cr, uid, [('name', 'like', i.origin)])
                res[i.id] = obj_sale_order.browse(cr, uid, src_sale_order[0], context)['operaciones']
                
            # Albaran de entrada, captura una compra
            if i.origin and i.type in ['in']:
                doc = i.origin.split(':')
                if doc:
                    src_purchase_order = obj_purchase_order.search(cr, uid, [('name', 'like', doc[0])])
                else:
                    src_purchase_order = obj_purchase_order.search(cr, uid, [('name', 'like', i.origin)])
                res[i.id] = obj_purchase_order.browse(cr, uid, src_purchase_order[0], context)['operaciones']
            
        return res
    
    _columns = {
        'pedimento_id': fields.many2one('import.info', 'Pedimento'),
        'perfiles_ids': fields.related('partner_id', 'answers_ids', 
            type='many2many', relation='crm_profiling.answer', 
            string='Perfiles'),
        'preentrada_id': fields.many2one('stock.picking.pre', 
            'Codigo de pre-entrada'),
        'cliente_ref': fields.char('Referencia cliente', size=1024),
        'efectua_id': fields.many2one('res.users', 'Efectua'),
        'operaciones': fields.function(_get_operacion, type='selection', 
            selection=[('linea','Operaciones de linea'), 
            ('desarrollo','Operaciones de desarrollo')], string='Operacion')
    }
    
stock_picking_out_esc()
