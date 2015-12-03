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
from datetime import *
import logging
_logger = logging.getLogger(__name__)

class stick_aprobado_esc(osv.Model):

    _name = 'stick.aprobado'
    _description = 'Creacion modelo Stick Aprobado para etiquetas de aprobado'
    
    # 09/04/2015 (felix) Metodo para generar correlativo de referencia de stick aprobado
    def _get_ref(self, cr, uid, context=None):
        res = {}
        prefijo = 'STICK/'
        ano = datetime.now().year
        all_rec = self.search(cr, uid, [(1, '=', 1)], order='id')
        if all_rec:
            for item in self.browse(cr, uid, all_rec, context):
                last_name = item.name.split('/')
                last_num = int(last_name[2]) + 1
                res = prefijo+str(ano)+'/'+str(last_num).rjust(6, '0')
        else:
            res = prefijo+str(ano)+'/'+str(1).rjust(6, '0')
        return res
    
    _columns = {
        'name': fields.char('Referencia etiqueta aprobado', size=250),
        'fecha_fabricacion': fields.date('Fecha de fabricacion'),
        'fecha_caducidad': fields.date('Fecha de caducidad'),
        'product_id': fields.many2one('product.product', 'Producto'),
        'lote_id': fields.many2one('stock.production.lot', 'Lote'),
        'peso_neto': fields.float('Peso neto', digits=(10,2)),
        'peso_bruto': fields.float('Peso bruto', digits=(10,2)),
        'peso_tara': fields.float('Tara', digits=(10,2))
    }
    _defaults = {
        'name': _get_ref
    }
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Este campo debe ser unico')
    ]
    
    # 09/04/2015 (felix) Calculo peso bruto
    def on_change_peso(self, cr, uid, ids, peso_neto=0.00, peso_tara=0.00, context=None):
        res = {}
        peso_bruto = peso_neto + peso_tara
        res = {'peso_bruto': peso_bruto}
        return {'value':res}
    
stick_aprobado_esc()
