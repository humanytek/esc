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

class stock_picking_pre_esc(osv.Model):

    _name = 'stock.picking.pre'
    _description = 'Creacion modelo Stock Picking Pre'
    
    # 08/04/2015 (felix) Metodo para generar correlativo de codigo de pre-entrada
    def _get_codigo(self, cr, uid, context=None):
        res = {}
        prefijo = 'PREIN/'
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
        
    # 15/04/2015 (felix) Metodo para generar total de cantidad kg por envases
    def _calc_totalenvases(self, cr, uid, ids, fields_name, args, context=None):
        res = {}
        if ids:
            for i in self.browse(cr, uid, ids, context):
                res[i.id] = 0.00
                for j in i.envases_ids:
                    res[i.id] = res[i.id] + (j.cant_envases * j.peso_neto)
        return res
    
    _columns = {
        'name': fields.char('Codigo pre-entrada', size=250),
        'product_id': fields.many2one('product.product', 'Producto'),
        'fecha_ingreso': fields.date('Fecha de ingreso'),
        'fecha_fabricacion': fields.date('Fecha de fabricacion'),
        'fecha_caducidad': fields.date('Fecha de caducidad'),
        'fecha_retest': fields.date('Fecha de retest'),
        'fabricante_id': fields.many2one('res.partner', 'Fabricante'),
        'proveedor_id': fields.many2one('res.partner', 'Proveedor', 
            domain=[('supplier', '=', True)]),
        'pedimento_id': fields.many2one('import.info', 'Pedimento No.'),
        'almacen_id': fields.many2one('stock.warehouse', 'Almacen'),
        'aduana_id': fields.many2one('import.info.custom', 'Aduana'),
        'lote_id': fields.many2one('stock.production.lot', 'Lote'),
        'orden_compra_id': fields.many2one('purchase.order', 'Orden de compra'),
        'factura_no': fields.char('Factura No.', size=1024),
        'cant_total': fields.float('Cantidad total', digits=(10,2)),
        'total_envases': fields.function(_calc_totalenvases, type='float', 
            string='Total'),
        'envases_ids': fields.one2many('stock.picking.envases', 'envases_id', 
            'Envases'),
        'stock_inspeccion_ids': fields.one2many('stock.picking.pre.inspeccion', 
            'stock_picking_pre_id', 'Inspeccion fisica'),
        'stock_preentrada_ids': fields.one2many('stock.move', 'preentrada_id', 
            'Pre-entrada/Stock Move')
    }
    _order = 'fecha_ingreso desc'
    _defaults = {
        'name': _get_codigo
    }
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Este campo debe ser unico')
    ]
            
    # 08/04/2015 (felix) Autocompletar campos relacionados con pedimento
    def on_change_pedimento(self, cr, uid, ids, pedimento_id, context=None):
        res = {}
        if pedimento_id:
            # Traer informacion de la tabla de pedimentos
            obj_import_info = self.pool.get('import.info')
            src_import_info = obj_import_info.search(cr, uid, [('id', '=', pedimento_id)])[0]
            aduana_id = obj_import_info.browse(cr, uid, src_import_info, context)['customs']['id']
            res = {
                'aduana_id': aduana_id
            }        
        return {'value':res}
        
    # 15/04/2015 (felix) Autocompletar campos relacionados con el producto
    def on_change_product(self, cr, uid, ids, product_id, context=None):
        res = {}
        if product_id:
            obj_product = self.pool.get('product.product')
            src_product = obj_product.search(cr, uid, [('id', '=', product_id)])
            fabricante = obj_product.browse(cr, uid, src_product[0], context)['manufacturer']
            res = {
                'fabricante_id': fabricante.id
            }
        return {'value':res}
        
    # 04/06/2015 (felix) Autocompletar campos relacionados con Lote
    def on_change_lote(self, cr, uid, ids, lote_id, context=None):
        res = {}
        obj_production_lot = self.pool.get('stock.production.lot')
        fecha_fabricacion = obj_production_lot.browse(cr, uid, lote_id, context=None)['date']
        fecha_caducidad = obj_production_lot.browse(cr, uid, lote_id, context=None)['use_date']
        fecha_retest = obj_production_lot.browse(cr, uid, lote_id, context=None)['alert_date']
        res = {
            'fecha_fabricacion': fecha_fabricacion,
            'fecha_caducidad': fecha_caducidad,
            'fecha_retest': fecha_retest,
        }        
        return {'value':res}
    
stock_picking_pre_esc()


class stock_picking_inspeccion_esc(osv.Model):

    _name = 'stock.picking.pre.inspeccion'
    _description = 'Modelo para crear lista de condiciones'
    _columns = {
        'name': fields.many2one('stock.picking.pre.condicion', 'Condicion'),
        'resultado': fields.char('Resultado', size=2048),
        'list_empaque': fields.boolean('Lista de empaque'),
        'orden_compra': fields.boolean('Orden de compra'),
        'factura': fields.boolean('Factura'),
        'cert_analisis': fields.boolean('Certificado de analisis'),
        'comentario': fields.text('Comentario u observacion', size=2048),
        'stock_picking_pre_id': fields.many2one('stock.picking.pre', 
            'Inspeccion fisica')
    }
    _order = 'name'

stock_picking_inspeccion_esc()


class stock_picking_envases_esc(osv.Model):

    _name = 'stock.picking.envases'
    _description = 'Envases por pre-entrada'
    
    # 15/04/2015 (felix) Calculo de subtotal de peso por cantidad de envases
    def _calc_subtotal_envases(self, cr, uid, ids, fields_name, args, context=None):
        res = {}
        for i in self.browse(cr, uid, ids, context):
            res[i.id] = 0.0
            res[i.id] = i.cant_envases * i.peso_neto
        return res
    
    _columns = {
        'cant_envases': fields.integer('Cantidad de envases'),
        'peso_neto': fields.float('Peso neto', digits=(10,2)),
        'peso_bruto': fields.float('Peso bruto', digits=(10,2)),
        'peso_tara': fields.float('Tara', digits=(10,2)),
        'subtotal_envases': fields.function(_calc_subtotal_envases, type='float',
            string='Subtotal N/Envases'),
        'envases_id': fields.many2one('stock.picking.pre', 'Envases')
    }
    
    # 15/04/2015 (felix) Calculo peso bruto
    def on_change_peso(self, cr, uid, ids, cant_envases=0, peso_bruto=0.00, peso_tara=0.00, context=None):
        res = {}
        peso_neto = peso_bruto - peso_tara
        res = {
            'peso_neto': peso_neto
        }
        return {'value':res}        
    
stock_picking_envases_esc()
