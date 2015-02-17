# -*- encoding: utf-8 -*
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
##############################################################################

from osv import fields,osv
from tools.translate import _
from datetime import datetime
import time

class date_wizard(osv.osv_memory):
    _name = "date.wizard"
    _columns = {
                'start_date': fields.date("Initial date"),
                'end_date': fields.date("Final date"),
                'journal_ids': fields.many2many("account.journal",'date_wizard_journals', 'sale_margin_id',
                                                'journal_id', "Journals"),
                'product_ids': fields.many2many("product.product", 'date_wizard_products', 'wizard_id',
                                                'product_id', "Products")
                }
    
    def view_account_sale_margin_action(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = self.browse(cr, uid, ids, context=context)[0]        
        context['start_date'] = data.start_date
        context['end_date'] = data.end_date
        product_ids =  [x.id for x in data.product_ids]
        journal_ids =  [x.id for x in data.journal_ids]
        if journal_ids == []:
            journal_ids = self.pool.get('account.journal').search(cr, uid, [], context=context)
        st_date = time.strftime('%Y-%m-%d', time.strptime(str(data.start_date), '%Y-%m-%d'))
        end_date = time.strftime('%Y-%m-%d', time.strptime(str(data.end_date), '%Y-%m-%d'))
#         context['type'] = data.type
        
#         pi_obj = self.pool.get('account.sale.margin')
#         pi_obj.generate_report(cr, uid, context)

        mod_obj = self.pool.get('ir.model.data')
 
        tree_res_id = mod_obj.get_object_reference(cr, uid, 'sfs_account_sale_margin', 'view_account_sale_margin_tree')[1]
#         tree_res_id = tree_res and tree_res[1] or False
        form_res_id = mod_obj.get_object_reference(cr, uid, 'sfs_account_sale_margin', 'view_account_sale_margin_form')[1]
#         form_res_id = form_res and form_res[1] or False
        self.pool.get('sale.margin_product').init(cr)
        vals = {
            'name': _('Sale Margin Analysis'),
            'domain' : [('date_invoice','>=',st_date), ('date_invoice','<=',end_date), 
                        ('product_id','not in',product_ids), ('account_journal_id','in', journal_ids)],
            'view_type': 'form',
            'view_mode': 'tree,form',
            'view_id': False,
            'views': [(tree_res_id or False, 'tree'),(form_res_id or False, 'form')
                    ],
            'res_model': 'sale.margin_product',
            'context': {},
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
        return vals

date_wizard()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:-