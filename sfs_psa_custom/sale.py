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
from openerp.tools.translate import _

class sale_oder(osv.osv):
    
    _inherit = 'sale.order'
    
    def _prepare_order_line_move(self, cr, uid, order, line, picking_id, date_planned, context=None):
        """Adds brand_id to related stock moves from the procurement related to the sale order """
        res = super(sale_oder, self)._prepare_order_line_move(cr, uid, order, line, picking_id, date_planned, context)
        res.update({'brand_id': line.brand_id and line.brand_id.id or False})
        return res
     
class sale_order_line(osv.osv):
    
    _inherit = 'sale.order.line'
    
    def _prepare_order_line_invoice_line(self, cr, uid, line, account_id=False, context=None):
        """Adds brand_id to created invoice lines from the sale order """
        res = super(sale_order_line, self)._prepare_order_line_invoice_line(cr, uid, line, account_id, context)
        res.update({'brand_id': line.brand_id and line.brand_id.id or False})
        return res
        
    def onchange_supplier_id(self, cr, uid, ids, supplier_id, date_order, pricelist, product, qty, uom, context=None):
        res ={}
        price = 0.00
        brand = False
        if supplier_id:
            supplier_id_rec = self.pool.get('product.supplierinfo').browse(cr, uid, supplier_id, context)
            supplier_id = supplier_id_rec.name.id
            if not pricelist:
                raise osv.except_osv(_('Warning!'),_("Select a pricelist for the sale order first"))
            else:
                price = self.pool.get('product.pricelist').price_get(cr, uid, [pricelist],
                            product, qty or 1.0, supplier_id, {
                                'uom': uom,
                                'date': date_order,
                                })[pricelist]
                brand = supplier_id_rec.brand_id and supplier_id_rec.brand_id.id or False
        res = {'value' : {'price_unit' : price, 'brand_id': brand}}       
        return res
    
    _columns = {
                'supplier_id': fields.many2one('product.supplierinfo','Suppliers', required=True),
                'brand_id': fields.many2one('product.brand', 'Brand')
                }
    
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
         
        res = super(sale_order_line, self).product_id_change(cr, uid, ids, pricelist, product, qty, uom, 
                                                             qty_uos, uos, name, partner_id, lang, update_tax, 
                                                             date_order, packaging, fiscal_position, flag, context)
        res['value'].update({'supplier_id': False})
        return res
    
    def view_info(self, cr, uid, ids, context= None):
        if context == None:
            context = {}
        if not context.get('product_id',False):
            raise osv.except_osv(_('Warning!'), (_('Please select a product first')))
        else:
            c = {}
            product_recs = self.pool.get('product.product').browse(cr, uid, context.get('product_id'), context=context)
            compose_form_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'sfs_psa_custom', 
                                                                                  'view_sale_order_line_info')[1]
            return {
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'sale.order.line.view.info',
                'views': [(compose_form_id, 'form')],
                'view_id': compose_form_id,
                'target': 'new',
                'context':  context
            }
        return False        

sale_order_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
