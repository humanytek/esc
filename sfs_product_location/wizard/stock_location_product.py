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

from lxml import etree
from openerp.osv.orm import setup_modifiers
from tools.translate import _

class stock_location_product(osv.osv):
    _inherit = 'stock.location.product'
    
    def fields_view_get(self, cr, user, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        if context is None:
            context = {}
        res = super(stock_location_product, self).fields_view_get(cr, user, view_id, view_type, context, toolbar,
                                                                  submenu)
        if context.get('active_id', False):
            arch = res['arch']
            doc = etree.XML(res['arch'])
            nodes = doc.xpath("//field[@name='location_id']")
            for node in nodes:
                node.set('invisible', 'True')
                node.set('required', 'False')
                setup_modifiers(node, res['fields']['location_id'])
            res['arch'] = etree.tostring(doc)
        return res
    
    _columns = {
                'location_id': fields.many2one('stock.location', 'Location')
                }
    
    def action_open_window(self, cr, uid, ids, context=None):
        """ To open location wise product information specific to given duration
         @param self: The object pointer.
         @param cr: A database cursor
         @param uid: ID of the user currently logged in
         @param ids: An ID or list of IDs (but only the first ID will be processed)
         @param context: A standard dictionary 
         @return: Invoice type
        """
        if context is None:
            context = {}
        location_products = self.read(cr, uid, ids, ['from_date', 'to_date', 'location_id'], context=context)
        if not context.get('active_id', False):
            location_data = location_products[0]['location_id']
            active_id = location_data and location_data[0] or False
        else:
            active_id = context.get('active_id', [])
        if location_products:
            return {
                    'name': _('Current Inventory'),
                    'view_type': 'form',
                    'view_mode': 'tree,form',
                    'res_model': 'product.product',
                    'type': 'ir.actions.act_window',
                    'context': {'location': active_id,
                                'from_date': location_products[0]['from_date'],
                       'to_date': location_products[0]['to_date']},
                    'domain': [('type', '<>', 'service')],
                    }
        
stock_location_product()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
