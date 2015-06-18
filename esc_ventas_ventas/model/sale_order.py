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

class sale_order_esc(osv.Model):

    _inherit = 'sale.order'
    _description = 'Personalizacion para lineas de pedidos en ordenes de venta'
    _columns = {
        'perfiles_ids': fields.related('partner_id', 'answers_ids', 
            type='many2many', relation='crm_profiling.answer', 
            string='Perfiles'),
        'operaciones': fields.selection([('linea','Operaciones de linea'), 
            ('desarrollo','Operaciones de desarrollo')], 'Operacion'),
    }
    
    # 18/06/2015 (felix) Modificado metodo original para discriminar el order_line
    def copy(self, cr, uid, id, default=None, context=None):
        if not default:
            default = {}
        _logger.warn('Valor de id %s', id)
        _logger.warn('Valor de default %s', default)
        _logger.warn('Valor de context %s', context)
        
        for i in self.browse(cr, uid, id, context):
            _logger.warn('Valor de order_line %s', i.order_line)
        '''
        default.update({
            'date_order': fields.date.context_today(self, cr, uid, context=context),
            'state': 'draft',
            'invoice_ids': [],
            'date_confirm': False,
            'client_order_ref': '',
            'name': self.pool.get('ir.sequence').get(cr, uid, 'sale.order'),
        })
        return super(sale_order_esc, self).copy(cr, uid, id, default, context=context)
        '''
    
sale_order_esc()
