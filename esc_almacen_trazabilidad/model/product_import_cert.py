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
    
    _columns = {
        'background_country_ids': fields.one2many('product.import.certificate.line', 
            'certificado_id', 'Backgrounds'),
        'move_ids': fields.one2many('stock.move', 'picking_id', 'Moves'),
        'qty_imported': fields.function(_calculate_qty, type='float', 
            string='Quantity Imported', digits=(10,3), 
            states={'not_extend':[('readonly',True)]}),
        'qty': fields.float('Quantity', digits=(10,3), 
            states={'not_extend':[('readonly',True)]}),
    }
    
product_import_certificate_esc()
