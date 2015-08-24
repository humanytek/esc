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

class stock_move_esc(osv.Model):

    _inherit = 'stock.move'
    _description = 'Cambios en campos y modelos para Stock Move'
    _columns = {
        'fecha_fabricacion': fields.datetime('Fecha de fabricacion'),
        'fecha_caducidad': fields.datetime('Fecha de caducidad'),
        'fecha_retest': fields.datetime('Fecha de retest'),
        'pedimento_id': fields.many2one('import.info', 'Pedimento'),
        'preentrada_id': fields.many2one('stock.picking.pre', 'Pre-entrada')
    }
    
    # 20/02/2015 (felix) Metodo original modificado para agregar campos:
    # - fecha de fabricacion
    # - fecha de caducidad
    # - fecha de retest
    def onchange_lot_id(self, cr, uid, ids, prodlot_id=False, product_qty=False,
                        loc_id=False, product_id=False, uom_id=False, context=None):
        """ On change of production lot gives a warning message.
        @param prodlot_id: Changed production lot id
        @param product_qty: Quantity of product
        @param loc_id: Location id
        @param product_id: Product id
        @return: Warning message
        """
        
        # Aviso si no ha seleccionado producto
        if not product_id:
            raise osv.except_osv(_('Warning!'),'No ha seleccionado un producto.')
            
        if not prodlot_id or not loc_id:
            return {}
        ctx = context and context.copy() or {}
        ctx['location_id'] = loc_id
        ctx.update({'raise-exception': True})
        uom_obj = self.pool.get('product.uom')
        product_obj = self.pool.get('product.product')
        product_uom = product_obj.browse(cr, uid, product_id, context=ctx).uom_id
        prodlot = self.pool.get('stock.production.lot').browse(cr, uid, prodlot_id, context=ctx)
        location = self.pool.get('stock.location').browse(cr, uid, loc_id, context=ctx)
        uom = uom_obj.browse(cr, uid, uom_id, context=ctx)
        amount_actual = uom_obj._compute_qty_obj(cr, uid, product_uom, prodlot.stock_available, uom, context=ctx)
        warning = {}
        if (location.usage == 'internal') and (product_qty > (amount_actual or 0.0)):
            warning = {
                'title': _('Insufficient Stock for Serial Number !'),
                'message': _('You are moving %.2f %s but only %.2f %s available for this serial number.') % (product_qty, uom.name, amount_actual, uom.name)
            }
        
        # Campos adicionales
        res = {}
        fecha_fabricacion = prodlot['date']
        fecha_caducidad = prodlot['use_date']
        fecha_retest = prodlot['alert_date']
        res = {
            'fecha_fabricacion':fecha_fabricacion,
            'fecha_caducidad': fecha_caducidad,
            'fecha_retest': fecha_retest
        }
        
        return {'warning': warning, 'value': res}
    
        
stock_move_esc()
