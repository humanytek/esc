# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2013 SF Soluciones.
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
##################################################
from osv import fields, osv
from openerp.tools import float_compare
from openerp.tools.translate import _

class stock_move(osv.osv):
    _inherit = 'stock.move'
    
    def action_done(self, cr, uid, ids, context=None):
        if context == None:
            context = {}
        group_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'sfs_stock_security', 'group_stock_force_availablity')[1]
        groups_obj = self.pool.get("res.users").browse(cr, uid, uid, context=context).groups_id
        group_ids = [x.id for x in groups_obj]
        if context.get('process_entirely_click',False) and context.get('process_entirely_click',False) == 1:
                for stm_obj in self.browse(cr, uid, ids, context=context):
                    qty = stm_obj.product_qty
                    product_obj = stm_obj.product_id
                    uom2 = stm_obj.product_uom
                    compare_qty = float_compare(product_obj.virtual_available * uom2.factor, qty * product_obj.uom_id.factor, precision_rounding=product_obj.uom_id.rounding)
                    if (product_obj.type=='product') and int(compare_qty) == -1 \
                        and (product_obj.procure_method=='make_to_stock') and stm_obj.state in ['confirmed','draft'] \
                        and group_id not in group_ids:
                        raise osv.except_osv(_('UserError'),('''You Must belong to group
                         "Allow force availablity" in order to process this Stock move'''))
        res = super(stock_move, self).action_done(cr, uid, ids, context=context)
        return res
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: