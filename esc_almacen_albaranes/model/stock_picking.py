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
import re
import logging
_logger = logging.getLogger(__name__)

class stock_picking_esc(osv.Model):

    _inherit = 'stock.picking'
    _description = 'Cambios en campos y modelos para Stock Picking'
        
    # 15/02/2016 (felix) Metodo para relacionar referencia cliente con referencia cliente de ventas
    def _get_ref_cliente(self, cr, uid, ids, fields_name, args, context=None):
        res = {}
        obj_sale = self.pool.get('sale.order')
        for i in self.browse(cr, uid, ids, context):
            res[i.id] = ''
            if i.sale_id:
                _logger.warn('Valor de sale_id %s', i.sale_id.id)
                get_sale = obj_sale.search(cr, uid, [('id', '=', i.sale_id.id)])
                if get_sale:
                    res[i.id] = obj_sale.browse(cr, uid, get_sale[0], context)['client_order_ref']
        return res
    
    _columns = {
        'pedimento_id': fields.many2one('import.info', 'Pedimento'),
        'perfiles_ids': fields.related('partner_id', 'answers_ids', 
            type='many2many', relation='crm_profiling.answer', 
            string='Perfiles'),
        'preentrada_id': fields.many2one('stock.picking.pre', 
            'Codigo de pre-entrada'),
        'cliente_ref': fields.function(_get_ref_cliente, type='char', 
            string='Referencia cliente', store=True),
        'efectua_id': fields.many2one('res.users', 'Efectua'),
        'operaciones': fields.selection([('linea','Operaciones de linea'), 
            ('desarrollo','Operaciones de desarrollo')], string='Operacion'),
        'certificate_number_id': fields.many2one('product.import.certificate', 
            'Import certificate number'),
    }
    
stock_picking_esc()


class stock_picking_in_esc(osv.Model):

    _inherit = 'stock.picking.in'
    _description = 'Cambios en campos y modelos para Stock Picking In'    
    _columns = {
        'pedimento_id': fields.many2one('import.info', 'Pedimento'),
        'preentrada_id': fields.many2one('stock.picking.pre', 
            'Codigo de pre-entrada'),
        'operaciones': fields.selection([('linea','Operaciones de linea'), 
            ('desarrollo','Operaciones de desarrollo')], string='Operacion'),
        'certificate_number_id': fields.many2one('product.import.certificate', 
            'Import certificate number'),
    }
    
stock_picking_in_esc()


class stock_picking_out_esc(osv.Model):

    _inherit = 'stock.picking.out'
    _description = 'Cambios en campos y modelos para Stock Picking Out'
        
    # 15/02/2016 (felix) Metodo para relacionar referencia cliente con referencia cliente de ventas
    def _get_ref_cliente(self, cr, uid, ids, fields_name, args, context=None):
        res = {}
        obj_sale = self.pool.get('sale.order')
        for i in self.browse(cr, uid, ids, context):
            res[i.id] = ''
            if i.sale_id:
                _logger.warn('Valor de sale_id %s', i.sale_id.id)
                get_sale = obj_sale.search(cr, uid, [('id', '=', i.sale_id.id)])
                if get_sale:
                    res[i.id] = obj_sale.browse(cr, uid, get_sale[0], context)['client_order_ref']
        return res
    
    _columns = {
        'pedimento_id': fields.many2one('import.info', 'Pedimento'),
        'perfiles_ids': fields.related('partner_id', 'answers_ids', 
            type='many2many', relation='crm_profiling.answer', 
            string='Perfiles'),
        'preentrada_id': fields.many2one('stock.picking.pre', 
            'Codigo de pre-entrada'),
        'cliente_ref': fields.function(_get_ref_cliente, type='char', 
            string='Referencia cliente', store=True),
        'efectua_id': fields.many2one('res.users', 'Efectua'),
        'operaciones': fields.selection([('linea','Operaciones de linea'), 
            ('desarrollo','Operaciones de desarrollo')], string='Operacion'),
        'certificate_number_id': fields.many2one('product.import.certificate', 
            'Import certificate number'),
    }
    
stock_picking_out_esc()
