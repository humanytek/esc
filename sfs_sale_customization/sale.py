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

from openerp.tools import float_compare
from tools.translate import _

class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'
    
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False,
            fiscal_position=False, flag=False, context=None):
        product_pool = self.pool.get('product.product')
        product_uom_obj = self.pool.get('product.uom')
        res = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty, uom, qty_uos,
                                                             uos, name, partner_id, lang, update_tax, date_order,
                                                             packaging, fiscal_position, flag, context=context)
        warning = {}
        if product:
            product_obj = product_pool.browse(cr, uid, product, context=context)
            uom2 = False
            if uom:
                uom2 = product_uom_obj.browse(cr, uid, uom)
                if product_obj.uom_id.category_id.id != uom2.category_id.id:
                    uom = False
            if not uom2:
                uom2 = product_obj.uom_id
            res_packing = self.product_packaging_change(cr, uid, ids, pricelist, product, qty, uom, partner_id, packaging, context=context)
            warning_msgs = res_packing.get('warning') and res_packing['warning']['message'] or ''
            compare_qty = float_compare(product_obj.qty_available * uom2.factor, qty * product_obj.uom_id.factor, precision_rounding=product_obj.uom_id.rounding)
            if (product_obj.type=='product') and int(compare_qty) == -1 \
              and (product_obj.procure_method=='make_to_stock'):
                warn_msg = _('You plan to sell %.2f %s but you only have %.2f %s available !\nThe real stock is %.2f %s. (without reservations)') % \
                        (qty, uom2 and uom2.name or product_obj.uom_id.name,
                         max(0,product_obj.qty_available), product_obj.uom_id.name,
                         max(0,product_obj.qty_available), product_obj.uom_id.name)
                warning_msgs += _("Not enough stock ! : ") + warn_msg + "\n\n"
            if warning_msgs:
                 warning = {
                            'title': _('Configuration Error!'),
                            'message' : warning_msgs
                            }
                 res.update({'warning': warning})
        return res
    
sale_order_line()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
