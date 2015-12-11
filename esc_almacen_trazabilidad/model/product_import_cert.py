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


class product_import_certificate_esc(osv.Model):

    _inherit = 'product.import.certificate'
    _description = 'Datos adicionales de permisos de importacion'
    
    # 17/06/2015 (felix) Metodo de los hindues, daba un error
    def unlink(self, cr, uid, ids, context=None):
        for i in self.browse(cr, uid, ids, context=context):
            if i.state != 'new':
                if i.state == 'not_extend':
                    raise osv.except_osv(_('Warning!'), _('You cannot do any operation in the record which is not extendable.'))
                else:
                    raise osv.except_osv(_('Warning!'), _('For deleting the record, the state should be in New.'))
        return super(product_import_certificate_esc, self).unlink(cr, uid, ids, context=context)
    
    # 17/06/2015 (felix) Metodo de los hindues, daba un error
    def change_state(self, cr, uid, ids,context=None):
        for i in self.browse(cr, uid, ids, context=context):
            if i.state == 'new':
                self.write(cr, uid, [i.id], {'state': 'active'}, context=context)
            if i.state == 'active':
                self.write(cr, uid, [i.id], {'state': 'in_renov'}, context=context)
            if i.state == 'in_renov':
                self.write(cr, uid, [i.id], {'state': 'renov', 'renewable': True,}, context=context)
            if i.state == 'renov':
                self.write(cr, uid, [i.id], {'state': 'spent'}, context=context)
            if i.state == 'spent':
                self.write(cr, uid, [i.id], {'state': 'not_extend'}, context=context)
        return True
    
    # 17/06/2015 (felix) Metodo de los hindues, daba un error
    def previous_state(self, cr, uid, ids,context=None):
        for i in self.browse(cr, uid, ids, context=context):
            if i.state == 'active':
                self.write(cr, uid, [i.id], {'state': 'new'}, context=context)
            if i.state == 'in_renov':
                self.write(cr, uid, [i.id], {'state': 'active'}, context=context)
            if i.state == 'renov':
                self.write(cr, uid, [i.id], {'state': 'in_renov'}, context=context)
            if i.state == 'spent':
                self.write(cr, uid, [i.id], {'state': 'renov'}, context=context)
        return True
    
    # 17/06/2015 (felix) Metodo de los hindues, daba un error
    def _calculate_days(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        diff_days = 0
        for i in self.browse(cr, uid, ids, context=context):
            res[i.id] = 0
            if i.end_term and i.initial_term:
                diff_days = datetime.strptime(i.end_term, '%Y-%m-%d')-datetime.strptime(i.initial_term, '%Y-%m-%d')
                diff_days = diff_days.days
            res[i.id] = diff_days
        return res
    
    # 17/06/2015 (felix) Metodo de los hindues, daba un error
    def _calculate_stock_qty(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        move_pool = self.pool.get('stock.move')
        stock_qty = 0.00
        for i in self.browse(cr, uid, ids, context=context):
            res[i.id] = 0.00
            move_lines = move_pool.search(cr, uid, [('certificate_id', '=', i.id)],  context=context)
            if move_lines:
                stock_qty = sum([move.product_qty for move in move_pool.browse(cr, uid, move_lines)])
                qty = i.qty
                stock_qty = stock_qty
            res[i.id] = stock_qty
        return res
    
    # 17/06/2015 (felix) Metodo de los hindues, daba un error
    def _calculate_qty(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        qty_imported = 0.00
        stock_qty = 0.00
        for i in self.browse(cr, uid, ids, context=context):
            res[i.id] = 0.00
            # 09/11/2015 (felix) Modificado para corregir un detalle en la captura de productos
            #move_lines = move_pool.search(cr, uid, [('certificate_id', '=', i.id), ('type', '=', 'in'), ('state','=', 'done')],  context=context)
            move_pool = self.pool.get('stock.move')
            obj_picking = self.pool.get('stock.picking.in')
            src_picking = obj_picking.search(cr, uid, [('certificate_number_id', '=', i.id), ('state','=', 'done'), ('type', '=', 'in')])
            if src_picking:
                for get_picking in obj_picking.browse(cr, uid, src_picking, context):
                    move_lines = move_pool.search(cr, uid, [('picking_id', '=', get_picking.id), ('product_id', '=', i.product_id.id), ('state','=', 'done')])
                    if move_lines:
                        stock_qty += sum([move.product_qty for move in move_pool.browse(cr, uid, move_lines)])
                        qty = i.qty
                        qty_imported = qty - stock_qty
                    else:
                        qty_imported = i.qty
            res[i.id] = qty_imported
        return res
    
    # 17/06/2015 (felix) Metodo de los hindues, daba un error
    def _line_state(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for i in self.browse(cr, uid, ids, context=context):
            res[i.id] = ''
            if i.diff_days < 60 and i.diff_days >= 45:
                res[i.id] = 'blue'
            elif i.diff_days < 45:
                res[i.id] = 'red'
        return res
        
    # 17/06/2015 (felix) Metodo de los hindues, daba un error
    def _qty_uom(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        qty_uom = ''
        for i in self.browse(cr, uid, ids, context=context):
            res[i.id] = ''
            if i.uom_id and i.qty:
                qty_uom = str(i.qty)+' / '+str(i.uom_id.name)
            res[i.id] = qty_uom
        return res
        
    # 20/08/2015 (felix) Captura de datos para lista de productos por numero de permiso de importacion
    def _get_move_in(self, cr, uid, ids, field_name, arg=None, context=None):
        res = {}
        if not ids:
            return res
        """
        for id in ids:
            res.setdefault(id, [])
        cr.execute('''SELECT DISTINCT ON (1) t3.* FROM product_import_certificate t1 \n'''
            '''INNER JOIN stock_picking t2 \n'''
            '''ON (t2.certificate_number_id = '''+str(ids[0])+''' AND t2.type='in' AND t2.state='done') \n'''
            '''INNER JOIN stock_move t3 \n'''
            '''ON (t3.picking_id = t2.id) \n'''
            '''ORDER BY t3.id;''')
        res_q = cr.fetchall()
        res_l = []
        for r in res_q:
            obj_move = self.pool.get('stock.picking')
            src_move = obj_move.search(cr, uid, [('id', '=', r[0])])
            get_move = obj_move.read(cr, uid, src_move, context)
            _logger.warn('Valor de get_move %s', get_move)
            res_l.append(r)
        _logger.warn('Valor de res_l %s', res_l)
        """
        _logger.warn('Valor de ids %s', ids)
        obj_picking = self.pool.get('stock.picking.in')
        src_picking = obj_picking.search(cr, uid, [('certificate_number_id', '=', ids[0]), ('type', '=', 'in'), ('state','=', 'done')])
        if src_picking:
            _logger.warn('Valor de src_picking %s', src_picking)
            id_picking = obj_picking.browse(cr, uid, src_picking[0], context)['id']
            obj_move = self.pool.get('stock.move')
            src_move = obj_move.search(cr, uid, [('picking_id', '=', id_picking)])
            if src_move:
                _logger.warn('Valor de src_move %s', src_move)
                get_move = obj_move.browse(cr, uid, src_move[0], context)
                _logger.warn('Valor de get_move %s', get_move)                
        return res
    
    _columns = {
        'background_country_ids': fields.one2many('product.import.certificate.line', 
            'certificado_id', 'Backgrounds'),
        #'move_ids': fields.function(_get_move_in, type='one2many',
        #    obj='stock.move', string='Moves'),
        'move_ids': fields.one2many('stock.move', 'picking_id', 'Moves'),
        'qty_imported': fields.function(_calculate_qty, type='float', 
            string='Quantity Imported', digits=(10,3), 
            states={'not_extend':[('readonly',True)]}),
        'qty': fields.float('Quantity', digits=(10,3), 
            states={'not_extend':[('readonly',True)]}),
    }
        
    
product_import_certificate_esc()
