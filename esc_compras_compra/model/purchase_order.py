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

import time
import pytz
from openerp import SUPERUSER_ID
from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp.osv import fields, osv
from openerp import netsvc
from openerp import pooler
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp
from openerp.osv.orm import browse_record, browse_null
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP
from openerp.tools.float_utils import float_compare
from lxml import etree
import logging
_logger = logging.getLogger(__name__)


class purchase_order_esc(osv.Model):

    # 06/03/2015 (felix) Genera formulario dinamico
    def _view_purchase_stage_fields(self, cr, uid, arch, context=None):
        context = context or {}
        obj_stage = self.pool.get('purchase.stage')
        all_stage = obj_stage.search(cr, uid, [(1, '=', 1)])
        grupos = []
        
        # Llenado de campos dinamicos
        for i in obj_stage.browse(cr, uid, all_stage, context):
            if i.activa:
                grupos.append(({'group':{'string': i.name}}))
                for j in i.campos_ids:
                    grupos.append(({'field': {'name':j.name,'string':j.field_description}}))
                
        # Construccion XML
        arbol = etree.XML(arch)
        page = arbol.find('.//page[@string="Etapas de pedidos de compra"]')
        for g in grupos:
            for j,n in g.items():
                if 'group' in j:
                    grupo = etree.SubElement(page,j)
                    for l,v in n.items():
                        grupo.set(l,v)
                        grupo_tree = arbol.find('.//group[@string="'+v+'"]')
                else:
                    campo = etree.SubElement(grupo_tree,j)
                    for l,v in n.items():                        
                        campo.set(l,v)
        arch = etree.tostring(arbol, encoding="utf-8")
        
        return arch
    
    # 10/03/2015 (felix) Genera instancia de campos en formulario dinamico
    def _view_purchase_stage_fields_gen(self, cr, uid, fields, context=None):
        obj_stage = self.pool.get('purchase.stage')
        all_stage = obj_stage.search(cr, uid, [(1, '=', 1)])
        res = fields
        for i in obj_stage.browse(cr, uid, all_stage, context):
            if i.activa:
                for j in i.campos_ids:
                    res[j.name] = { 'type': j.ttype, 'string': j.field_description, 'views': {}, 'selectable':True }
        return res
    
    # 06/03/2015 (felix) Captura de campos para generar formulario dinamico
    def fields_view_get(self, cr, uid, view_id=None, view_type='form', context=None, toolbar=False, submenu=False):
        res = super(purchase_order_esc, self).fields_view_get(cr, uid, view_id, view_type, context, 
            toolbar=toolbar, submenu=submenu)
        if view_type == 'form':
            res['arch'] = self._view_purchase_stage_fields(cr, uid, res['arch'], context)
            res['fields'] = self._view_purchase_stage_fields_gen(cr, uid, res['fields'], context)
        return res
        
    _inherit = 'purchase.order'
    _description = 'Campos y metodos para el modulo de compras'
    _columns = {
        'purchase_stage_id': fields.many2one('purchase.stage', 
            'Etapas pedidos de compra', domain=[('activa', '=', True)]),
        'operaciones': fields.selection([('linea','Operaciones de linea'), 
            ('desarrollo','Operaciones de desarrollo')], 'Operacion'),
    }
        
purchase_order_esc()


class purchase_order_line_esc(osv.Model):

    _inherit = 'purchase.order.line'
    _description = 'Campos adicionales por linea de orden de compra'
    _columns = {
        'empresa_id': fields.many2one('res.company', 'Facturar a'),
        'rfc_empresa': fields.char('RFC empresa', size=5000),
        'aduana_id': fields.many2one('import.info.custom', 'Aduana'),
        'proveedor_id': fields.many2one('res.partner', 'Consignar a'),
        'rfc_proveedor': fields.char('RFC proveedor', size=5000),
        'contacto_ids': fields.one2many('res.partner', 'partner_purchase_line_id', 
            'Contactos'),
        'incoterm': fields.many2one('stock.incoterms', 'Incoterm'),
        'ciudad_id': fields.many2one('res.country.state.city', 'Destino final'),
        'estado_id': fields.many2one('res.country.state', 'Destino final'),        
        'manufacturer_id': fields.many2one('res.partner', 'Fabricante'),
        'fraccion_id': fields.many2one('product.tarrif_fraction', 
            'Fraccion arancelaria'),
        'requiere_permiso': fields.boolean('Requiere permiso'),
        'certificate_number': fields.many2one('product.import.certificate', 
            'Numero de permiso'),
        'fecha_vigencia': fields.char('Fecha de vigencia permiso'),
        #'procedencia_id': fields.many2one('product.import.certificate.line',
        #    'Procedencia'),
        'procedencia_id': fields.related('certificate_number', 
            'background_country_ids', type='one2many', 
            relation='product.import.certificate.line', string='Procedencias'),
        'notas_embarque': fields.text('Notas de embarque', size=5096),
        'tipo_venta': fields.char('Tipo de venta', size=2048),
        'operaciones': fields.char('Operaciones', size=2048),
        'linea': fields.char('Linea', size=2048)
    }
    
    # 13/04/2015 (felix) On change de proveedor para llenar campos RFC
    def on_change_proveedor(self, cr, uid, ids, proveedor_id, context=None):
        res = {}
        if proveedor_id:
            obj_partner = self.pool.get('res.partner')
            src_partner = obj_partner.search(cr, uid, [('id', '=', proveedor_id)])
            rfc_proveedor = obj_partner.browse(cr, uid, src_partner[0], context)['vat']
            res = {
                'rfc_proveedor': rfc_proveedor
            }
        return {'value':res}
        
    # 22/04/2015 (felix) On change de empresa para llenar campos RFC
    def on_change_empresa(self, cr, uid, ids, empresa_id, context=None):
        res = {}
        if empresa_id:
            obj_partner = self.pool.get('res.partner')
            src_partner = obj_partner.search(cr, uid, [('id', '=', empresa_id)])
            rfc_empresa = obj_partner.browse(cr, uid, src_partner[0], context)['vat']
            res = {
                'rfc_empresa': rfc_empresa
            }
        return {'value':res}
        
    # 24/04/2015 (felix) On change de numero de permiso
    def on_change_permiso(self, cr, uid, ids, certificate_number, context=None):
        res = {}
        obj_permiso_import = self.pool.get('product.import.certificate')
        src_permiso_import = obj_permiso_import.search(cr, uid, [('id', '=', certificate_number)])
        fecha_vigencia = obj_permiso_import.browse(cr, uid, src_permiso_import[0], context)['end_term']
        res = {
            'fecha_vigencia': fecha_vigencia
        }
        return {'value':res}
    
    # 13/04/2015 (felix) Metodo original para agregar fabricante de producto por defecto
    def onchange_product_id(self, cr, uid, ids, pricelist_id, product_id, qty, uom_id,
            partner_id, date_order=False, fiscal_position_id=False, date_planned=False,
            name=False, price_unit=False, context=None):
        """
        onchange handler of product_id.
        """
        if context is None:
            context = {}

        res = {'value': {'price_unit': price_unit or 0.0, 'name': name or '', 'product_uom' : uom_id or False}}
        if not product_id:
            return res

        product_product = self.pool.get('product.product')
        product_uom = self.pool.get('product.uom')
        res_partner = self.pool.get('res.partner')
        product_supplierinfo = self.pool.get('product.supplierinfo')
        product_pricelist = self.pool.get('product.pricelist')
        account_fiscal_position = self.pool.get('account.fiscal.position')
        account_tax = self.pool.get('account.tax')

        # - check for the presence of partner_id and pricelist_id
        #if not partner_id:
        #    raise osv.except_osv(_('No Partner!'), _('Select a partner in purchase order to choose a product.'))
        #if not pricelist_id:
        #    raise osv.except_osv(_('No Pricelist !'), _('Select a price list in the purchase order form before choosing a product.'))

        # - determine name and notes based on product in partner lang.
        context_partner = context.copy()
        if partner_id:
            lang = res_partner.browse(cr, uid, partner_id).lang
            context_partner.update( {'lang': lang, 'partner_id': partner_id} )
        product = product_product.browse(cr, uid, product_id, context=context_partner)
        #call name_get() with partner in the context to eventually match name and description in the seller_ids field
        if not name or not uom_id:
            # The 'or not uom_id' part of the above condition can be removed in master. See commit message of the rev. introducing this line.
            dummy, name = product_product.name_get(cr, uid, product_id, context=context_partner)[0]
            if product.description_purchase:
                name += '\n' + product.description_purchase
            res['value'].update({'name': name})

        # - set a domain on product_uom
        res['domain'] = {'product_uom': [('category_id','=',product.uom_id.category_id.id)]}

        # - check that uom and product uom belong to the same category
        product_uom_po_id = product.uom_po_id.id
        if not uom_id:
            uom_id = product_uom_po_id

        if product.uom_id.category_id.id != product_uom.browse(cr, uid, uom_id, context=context).category_id.id:
            if context.get('purchase_uom_check') and self._check_product_uom_group(cr, uid, context=context):
                res['warning'] = {'title': _('Warning!'), 'message': _('Selected Unit of Measure does not belong to the same category as the product Unit of Measure.')}
            uom_id = product_uom_po_id

        res['value'].update({'product_uom': uom_id})

        # - determine product_qty and date_planned based on seller info
        if not date_order:
            date_order = fields.date.context_today(self,cr,uid,context=context)


        supplierinfo = False
        precision = self.pool.get('decimal.precision').precision_get(cr, uid, 'Product Unit of Measure')
        for supplier in product.seller_ids:
            if partner_id and (supplier.name.id == partner_id):
                supplierinfo = supplier
                if supplierinfo.product_uom.id != uom_id:
                    res['warning'] = {'title': _('Warning!'), 'message': _('The selected supplier only sells this product by %s') % supplierinfo.product_uom.name }
                min_qty = product_uom._compute_qty(cr, uid, supplierinfo.product_uom.id, supplierinfo.min_qty, to_uom_id=uom_id)
                if float_compare(min_qty , qty, precision_digits=precision) == 1: # If the supplier quantity is greater than entered from user, set minimal.
                    if qty:
                        res['warning'] = {'title': _('Warning!'), 'message': _('The selected supplier has a minimal quantity set to %s %s, you should not purchase less.') % (supplierinfo.min_qty, supplierinfo.product_uom.name)}
                    qty = min_qty
        dt = self._get_date_planned(cr, uid, supplierinfo, date_order, context=context).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
        qty = qty or 1.0
        res['value'].update({'date_planned': date_planned or dt})
        if qty:
            res['value'].update({'product_qty': qty})

        # - determine price_unit and taxes_id
        if pricelist_id:
            price = product_pricelist.price_get(cr, uid, [pricelist_id],
                    product.id, qty or 1.0, partner_id or False, {'uom': uom_id, 'date': date_order})[pricelist_id]
        else:
            price = product.standard_price

        taxes = account_tax.browse(cr, uid, map(lambda x: x.id, product.supplier_taxes_id))
        fpos = fiscal_position_id and account_fiscal_position.browse(cr, uid, fiscal_position_id, context=context) or False
        taxes_ids = account_fiscal_position.map_tax(cr, uid, fpos, taxes)
        res['value'].update({'price_unit': price, 'taxes_id': taxes_ids})
        
        # 13/04/2015 (felix) Cargar valor de fabricante del producto
        if product['manufacturer']['name']:
            res['value'].update({'manufacturer_id':product['manufacturer']['id']})
            
        # 14/04/2015 (felix) Cargar valores de linea, tipo_venta, operaciones
        if product:
            res['value'].update({'tipo_venta':product['tipo_venta']})
            res['value'].update({'linea':product['linea']})
            res['value'].update({'operaciones':product['operaciones']})
            res['value'].update({'fraccion_id':product['fraccion_id']['id']})
            if product['import_certificate'] == True:
                res['value'].update({'requiere_permiso': True})

        return res
    
purchase_order_line_esc()
