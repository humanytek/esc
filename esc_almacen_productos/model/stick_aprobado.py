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
import openerp.addons.decimal_precision as dp
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
        'fecha_fabricacion': fields.char('Fecha de fabricacion'),
        'fecha_caducidad': fields.char('Fecha de caducidad'),
        'fecha_retest': fields.char('Fecha de retest'),
        'product_id': fields.many2one('product.product', 'Producto'),
        'lote_id': fields.many2one('stock.production.lot', 'Lote'),
        'peso_neto': fields.float('Peso neto', digits=(10,3)),
        'peso_neto_uom_id': fields.many2one('product.uom', 'Unidad peso neto'),
        'peso_bruto': fields.float('Peso bruto', digits=(10,3)),
        'peso_bruto_uom_id': fields.many2one('product.uom', 'Unidad peso bruto'),
        'peso_tara': fields.float('Tara', digits=(10,3)),
        'peso_tara_uom_id': fields.many2one('product.uom', 'Unidad peso tara'),
        'nota': fields.text('Nota'),
        'product_text': fields.char('Producto', size=2048),
        'estatus': fields.selection([('cuarentena', 'Cuarentena'), 
            ('aprobado', 'Aprobado'), ('rechazado', 'Rechazado')], 'Estatus'),
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
        
    # 16/02/2016 (felix) Relacion mes numerico y literal
    def _rel_mes(self, mes):
        mes_lit = ''
        if mes == '01':
            mes_lit = 'Ene'
        elif mes == '02':
            mes_lit = 'Feb'
        elif mes == '03':
            mes_lit = 'Mar'
        elif mes == '04':
            mes_lit = 'Abr'
        elif mes == '05':
            mes_lit = 'May'
        elif mes == '06':
            mes_lit = 'Jun'
        elif mes == '07':
            mes_lit = 'Jul'
        elif mes == '08':
            mes_lit = 'Ago'
        elif mes == '09':
            mes_lit = 'Sep'
        elif mes == '10':
            mes_lit = 'Oct'
        elif mes == '11':
            mes_lit = 'Nov'
        elif mes == '12':
            mes_lit = 'Dic'
        return mes_lit
        
    # 16/02/2016 (felix) Captura de fechas de lote para cambiar sus respectivos formatos
    def on_change_lote(self, cr, uid, ids, lote_id, context=None):
        res = {}
        obj_stock_prod_lot = self.pool.get('stock.production.lot')
        if lote_id:
            get_lote = obj_stock_prod_lot.search(cr, uid, [('id', '=', lote_id)])
            for i in obj_stock_prod_lot.browse(cr, uid, get_lote, context):
                if i.date:
                    fabricacion_mes = self._rel_mes(i.date[5:7])
                    fabricacion_ano = i.date[:4]
                else:
                    fabricacion_mes = ''
                    fabricacion_ano = ''
                
                if i.use_date:
                    caducidad_mes = self._rel_mes(i.use_date[5:7])
                    caducidad_ano = i.use_date[:4]
                else:
                    caducidad_mes = ''
                    caducidad_ano = ''
                
                if i.alert_date:
                    retest_mes = self._rel_mes(i.alert_date[5:7])
                    retest_ano = i.alert_date[:4]
                else:
                    retest_mes = ''
                    retest_ano = ''
                
                res = {
                    'fecha_fabricacion': fabricacion_mes+' '+fabricacion_ano,
                    'fecha_caducidad': caducidad_mes+' '+caducidad_ano,
                    'fecha_retest': retest_mes+' '+retest_ano,
                }
                
        return {'value':res}
    
stick_aprobado_esc()
