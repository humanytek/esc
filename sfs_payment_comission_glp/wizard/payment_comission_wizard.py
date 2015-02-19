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

class payment_commission_wizard(osv.osv_memory):
    _name = 'payment.comission.wizard'
    _description = 'Wizard to filter payment commission report'
    _columns = {
                'from_date': fields.date('Initial Date'),
                'to_date': fields.date('Final Date'),
                'user_id': fields.many2one('res.users', 'Salesperson')
                }
    
    def report_preview(self, cr, uid, ids, context=None):
        obj_model = self.pool.get('ir.model.data')
        domain = []
        data = self.read(cr, uid, ids, [], context=context)[0]
        if data.get('from_date', False):
            domain.append(('payment_date', '>=', data['from_date']))
        if data.get('to_date', False):
            domain.append(('payment_date', '<=', data['to_date']))
        if data.get('user_id', False):
            domain.append(('user_id', '=', data['user_id'][0]))
        model_data_ids = obj_model.search(cr,uid,[('model','=','ir.ui.view'),('name','=','view_payment_comission_report_tree')])
        resource_id = obj_model.read(cr, uid, model_data_ids, fields=['res_id'])[0]['res_id']
        search_model_data_ids = obj_model.search(cr,uid,[('model','=','ir.ui.view'),('name','=','view_payment_comission_report_search')])
        search_resource_id = obj_model.read(cr, uid, search_model_data_ids, fields=['res_id'])[0]['res_id']
        self.pool.get('payment.comission.report').init(cr)
        return {
                'name': _('Payment Commission'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'views': [(resource_id, 'tree')],
                'res_model': 'payment.comission.report',
                'type': 'ir.actions.act_window',
                'domain': domain,
                'context': context,
                'search_view_id': search_resource_id
                }
    
payment_commission_wizard()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
