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

from tools.translate import _

class stock_location_product_wizard(osv.osv_memory):
    _name = 'stock.location.product.wizard'
    _description = 'Wizard to select product for stock analysis'
    _columns = {
                'product_ids': fields.many2many('product.product', 'product_wizard_rel', 'wizard_id',
                                                'product_id', 'Products')
                }
    
    def create_report(self, cr, uid, ids, context=None):
        obj_model = self.pool.get('ir.model.data')
        data = self.read(cr, uid, ids, [])[0]
        product_ids = data.get('product_ids', [])
        model_data_ids = obj_model.search(cr, uid, [('model', '=', 'ir.ui.view'),
                                                    ('name', '=', 'view_stock_location_product_tree')])
        resource_id = obj_model.read(cr, uid, model_data_ids, fields=['res_id'])[0]['res_id']
        search_model_data_ids = obj_model.search(cr, uid, [('model', '=', 'ir.ui.view'),
                                                           ('name', '=', 'view_stock_location_product_search')])
        search_resource_id = obj_model.read(cr, uid, model_data_ids, fields=['res_id'])[0]['res_id']
        self.pool.get('stock.product.location').init(cr)
        return {
                'name': _('Stock Multyproduct'),
                'view_type': 'form',
                'view_mode': 'tree',
                'views': [(resource_id, 'tree')],
                'res_model': 'stock.product.location',
                'type': 'ir.actions.act_window',
                'domain': [('product_id', 'in', product_ids)],
                'context': context,
                'search_view_id': search_resource_id
                }

stock_location_product_wizard()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
