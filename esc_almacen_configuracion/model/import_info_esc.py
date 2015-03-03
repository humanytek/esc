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

class import_info_custom_esc(osv.Model):

    _inherit = 'import.info.custom'
    _columns = {
        'custom_number': fields.integer('Custom Number'),
        'description': fields.char('Descripcion', size=250)
    }
    _sql_constraints = [
        ('custom_number_uniq', 'unique(custom_number)', 'Referencia unica por numero de aduana')
    ]
    
    # 19/02/2015 (felix) Para concatenar numero y nombre de Aduana en la vista
    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if not ids:
            return []
        reads = self.read(cr, uid, ids, ['custom_name','custom_number'], context=context)
        res = []
        for record in reads:
            name = record['custom_name']
            number = record['custom_number']
            if name and number:
                
                name = '[ '+str(number)+' ] - '+name
            elif name and  not number:
                name = '[ '+name+' ]'
            elif number and not name:
                name = '[ '+str(number)+' ]'
            res.append((record['id'], name))
        return res

import_info_custom_esc()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
