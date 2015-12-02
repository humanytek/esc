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

class cert_analisis_esc(osv.Model):

    _name = 'cert.analisis'
    _description = 'Creacion modelo Certificados de analisis'
    
    # 10/04/2015 (felix) Metodo para generar correlativo de codigo de pre-entrada
    def _get_codigo(self, cr, uid, context=None):
        res = {}
        prefijo = 'CERT/'
        ano = datetime.now().year
        all_rec = self.search(cr, uid, [(1, '=', 1)], order='id')
        if all_rec:
            for item in self.browse(cr, uid, all_rec, context):
                last_name = item.name.split('/')
                last_num = int(last_name[2]) + 1
                res = prefijo+str(ano)+'/'+str(last_num).rjust(5, '0')
        else:
            res = prefijo+str(ano)+'/'+str(1).rjust(5, '0')
        return res
    
    _columns = {
        'name': fields.char('Certificado de analisis', size=250),
        'fecha_expedicion': fields.char('Fecha de expedicion', size=10),
        'fecha_fabricacion': fields.char('Fecha de fabricacion', size=10),
        'fecha_reanalisis': fields.char('Fecha de reanalisis', size=10),
        'fecha_caducidad': fields.char('Fecha de caducidad', size=10),
        'lote': fields.char('Lote', size=5000),
        'certificado': fields.char('Certificado', size=1024),
        'product_id': fields.char('Producto', size=5000),
        'informacion': fields.text('Informacion adicional'),
        'informacion_1': fields.text('Informacion adicional'),
        'firma': fields.char('Firma', size=2048),
        'resp_sanitario': fields.char('Resp. Sanitario', size=1024),
        'cod_product': fields.char('Codigo producto', size=5000),
        'pedido_compra': fields.char('Pedido de compra', size=5000),
        'cert_line_ids': fields.one2many('cert.analisis.line', 
            'cert_analisis_id', 'Pruebas/Especificaciones')
    }
    _order = 'fecha_reanalisis desc'
    _defaults = {
        'name': _get_codigo
    }
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Este campo debe ser unico')
    ]
    
cert_analisis_esc()


class cert_analisis_line_esc(osv.Model):

    _name = 'cert.analisis.line'
    _description = 'Listados de pruebas en certificados de analisis'
    _columns = {
        'name': fields.many2one('cert.analisis.test', 'Prueba'),
        'especificacion': fields.char('Especificacion', size=2048),
        'resultado': fields.char('Resultado', size=2048),
        'cert_analisis_id': fields.many2one('cert.analisis', 
            'Certificado de analisis')
    }
    
    # 10/04/2015 (felix) Autocompletado para linea de pruebas
    def on_change_prueba(self, cr, uid, ids, name, context=None):
        res = {}
        if name:
            obj_cert_test = self.pool.get('cert.analisis.test')
            src_cert_test = obj_cert_test.search(cr, uid, [('id', '=', name)])
            especificacion = obj_cert_test.browse(cr, uid, src_cert_test[0], context)['especificacion']
            res = {'especificacion':especificacion}
        return {'value':res}
                
    
cert_analisis_line_esc()
