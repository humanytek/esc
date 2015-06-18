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
from lxml import etree
import codecs
import logging
_logger = logging.getLogger(__name__)


class product_product_esc(osv.Model):

    _inherit = 'product.product'
    _description = 'Cambios y desarrollos para modulo de Productos'
    _columns = {
        'producto_cliente_ids': fields.one2many('product.cliente', 
            'producto_cliente_id', 'Datos del producto por cliente'),
        'operaciones': fields.selection([('linea','Operaciones de linea'), 
            ('desarrollo','Operaciones de desarrollo')], 'Operacion'),
        'linea': fields.selection([('humana','Humana'), 
            ('veterinaria','Veterinaria')], 'Línea'),
        'tipo_venta': fields.selection([('esic','ESIC'), 
            ('chemo','Grupo CHEMO')], 'Tipo de venta'),
        'fraccion_id': fields.many2one('product.tarrif_fraction', 
            'Fracción arancelaria')
    }

product_product_esc()


class product_cliente_esc(osv.Model):
    
    _name = 'product.cliente'
    _description = 'Datos de producto por cliente'
    _columns = {
        'name': fields.char('Nombre de producto', siez=1024),
        'especificacion': fields.char('Especificacion', siez=2048),
        'codigo_prod': fields.char('Codigo de producto', size=250),
        'cliente_id': fields.many2one('res.partner', 'Clientes', 
            domain=[('customer', '=', True)]),
        'producto_cliente_id': fields.many2one('product.product', 
            'Datos del producto por cliente'),
        'caducidad_id': fields.many2one('product.cliente.caducidad', 
            'Fecha minima de caducidad'),
        'cond_entrega': fields.char('Condicion de entrega', size=1024)
    }
    
product_cliente_esc()


class product_cliente_caducidad_esc(osv.Model):
    
    _name = 'product.cliente.caducidad'
    _description = 'Conjunto referencia y unidad de caducidad minima de producto'
    _columns = {
        'name': fields.char('Cantidad de caducidad minima', size=250),
        'unidad_cad_id': fields.many2one('product.uom', 'Unidad de caducidad', 
            domain=[('category_id.name', 'like', 'Caducidad de producto')])
    }
    
    # 08/04/2015 (felix) Para concatenar cantidad y unidad de caducidad de producto
    def name_get(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        if not ids:
            return []
        reads = self.read(cr, uid, ids, ['name','unidad_cad_id'], context=context)
        res = []
        for record in reads:
            nom = record['name']
            cad = record['unidad_cad_id'][1]
            if nom and cad:
                name = str(nom)+' '+cad
            res.append((record['id'], name))
        return res
    
product_cliente_caducidad_esc()
