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

class sale_order_line_esc(osv.Model):

    _inherit = 'sale.order.line'
    _description = 'Personalizacion para lineas de pedidos en ordenes de venta'    
    _columns = {
        'fecha_entrega': fields.date('Fecha de entrega'),
        'fecha_pedido': fields.date('Fecha de pedido'),
        'cant_desglose': fields.float('Cantidad desglose', digits=(10,2)),
        'cod_name_prod': fields.char('Codigo y nombre del producto', size=2048),
        'parent_line_id': fields.integer('Producto padre'),
        'product_desglose': fields.boolean('-'),
        'tipo_venta': fields.char('Tipo de venta', size=2048),
        'operaciones': fields.char('Operaciones', size=2048),
        'linea': fields.char('Linea', size=2048)
    }
    
    # 27/03/2015 (felix) Agregada opcion con orden de nombre de producto
    _order = 'order_id desc, name, sequence, id'
    
    # 17/03/2015 (felix) Cambio en on_change original para enviar codigo y nombre del producto segun el cliente
    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
            uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False, fiscal_position=False, flag=False, context=None):
        context = context or {}
        lang = lang or context.get('lang',False)
        if not  partner_id:
            raise osv.except_osv(_('No Customer Defined!'), _('Before choosing a product,\n select a customer in the sales form.'))
        warning = {}
        product_uom_obj = self.pool.get('product.uom')
        partner_obj = self.pool.get('res.partner')
        product_obj = self.pool.get('product.product')
        context = {'lang': lang, 'partner_id': partner_id}
        if partner_id:
            lang = partner_obj.browse(cr, uid, partner_id).lang
        context_partner = {'lang': lang, 'partner_id': partner_id}

        if not product:
            return {'value': {'th_weight': 0,
                'product_uos_qty': qty}, 'domain': {'product_uom': [],
                   'product_uos': []}}
        if not date_order:
            date_order = time.strftime(DEFAULT_SERVER_DATE_FORMAT)

        result = {}
        warning_msgs = ''
        product_obj = product_obj.browse(cr, uid, product, context=context_partner)

        uom2 = False
        if uom:
            uom2 = product_uom_obj.browse(cr, uid, uom)
            if product_obj.uom_id.category_id.id != uom2.category_id.id:
                uom = False
        if uos:
            if product_obj.uos_id:
                uos2 = product_uom_obj.browse(cr, uid, uos)
                if product_obj.uos_id.category_id.id != uos2.category_id.id:
                    uos = False
            else:
                uos = False
        fpos = fiscal_position and self.pool.get('account.fiscal.position').browse(cr, uid, fiscal_position) or False
        if update_tax: #The quantity only have changed
            result['tax_id'] = self.pool.get('account.fiscal.position').map_tax(cr, uid, fpos, product_obj.taxes_id)

        if not flag:
            result['name'] = self.pool.get('product.product').name_get(cr, uid, [product_obj.id], context=context_partner)[0][1]
            if product_obj.description_sale:
                result['name'] += '\n'+product_obj.description_sale
        domain = {}
        if (not uom) and (not uos):
            result['product_uom'] = product_obj.uom_id.id
            if product_obj.uos_id:
                result['product_uos'] = product_obj.uos_id.id
                result['product_uos_qty'] = qty * product_obj.uos_coeff
                uos_category_id = product_obj.uos_id.category_id.id
            else:
                result['product_uos'] = False
                result['product_uos_qty'] = qty
                uos_category_id = False
            result['th_weight'] = qty * product_obj.weight
            domain = {'product_uom':
                        [('category_id', '=', product_obj.uom_id.category_id.id)],
                        'product_uos':
                        [('category_id', '=', uos_category_id)]}
        elif uos and not uom: # only happens if uom is False
            result['product_uom'] = product_obj.uom_id and product_obj.uom_id.id
            result['product_uom_qty'] = qty_uos / product_obj.uos_coeff
            result['th_weight'] = result['product_uom_qty'] * product_obj.weight
        elif uom: # whether uos is set or not
            default_uom = product_obj.uom_id and product_obj.uom_id.id
            q = product_uom_obj._compute_qty(cr, uid, uom, qty, default_uom)
            if product_obj.uos_id:
                result['product_uos'] = product_obj.uos_id.id
                result['product_uos_qty'] = qty * product_obj.uos_coeff
            else:
                result['product_uos'] = False
                result['product_uos_qty'] = qty
            result['th_weight'] = q * product_obj.weight        # Round the quantity up

        if not uom2:
            uom2 = product_obj.uom_id
        # get unit price

        if not pricelist:
            warn_msg = _('You have to select a pricelist or a customer in the sales form !\n'
                    'Please set one before choosing a product.')
            warning_msgs += _("No Pricelist ! : ") + warn_msg +"\n\n"
        else:
            price = self.pool.get('product.pricelist').price_get(cr, uid, [pricelist],
                    product, qty or 1.0, partner_id, {
                        'uom': uom or result.get('product_uom'),
                        'date': date_order,
                        })[pricelist]
            if price is False:
                warn_msg = _("Cannot find a pricelist line matching this product and quantity.\n"
                        "You have to change either the product, the quantity or the pricelist.")

                warning_msgs += _("No valid pricelist line found ! :") + warn_msg +"\n\n"
            else:
                result.update({'price_unit': price})
        if warning_msgs:
            warning = {
                       'title': _('Configuration Error!'),
                       'message' : warning_msgs
                    }
                    
        # 17/03/2015 (felix) Enviar codigo y nombre del producto segun el cliente
        if partner_id:
            obj_product_cliente = self.pool.get('product.cliente')
            
            # 17/06/2015 (felix) Verifica si el cliente es contacto o empresa
            if partner_obj.browse(cr, uid, partner_id).type in ['contact']:
                contacto_id = partner_obj.browse(cr, uid, partner_id).parent_id.id
                src_product_cliente = obj_product_cliente.search(cr, uid, [('cliente_id', '=', contacto_id), ('producto_cliente_id', '=', product)])
            else:
                src_product_cliente = obj_product_cliente.search(cr, uid, [('cliente_id', '=', partner_id), ('producto_cliente_id', '=', product)])
                
            result['cod_name_prod'] = ''
            for i in obj_product_cliente.browse(cr, uid, src_product_cliente, context):
                result['cod_name_prod'] = '['+i.codigo_prod+'] '+i.name
                
            if not result['cod_name_prod']:
                raise osv.except_osv('Aviso','No existe codigo y nombre del producto definido por el cliente.\nDebe crearse el registro en:\nAlmacen/Productos/Productos/Datos del producto por cliente')
                
        # 06/04/2015 (felix) Igualar cantidad de desglose inicial a cantidad total de producto
        result['cant_desglose'] = qty
        
        # 14/04/2015 (felix) Cargar valores de linea, operaciones y tipo de venta
        result['tipo_venta'] = product_obj.tipo_venta
        result['linea'] = product_obj.linea
        result['operaciones'] = product_obj.operaciones
                    
        return {'value': result, 'domain': domain, 'warning': warning}
    
    
    # 19/03/2015 (felix) Metodo para desglose de entrega de productos Ventas/Ventas/Pedidos de Ventas
    def hacer_entrega(self, cr, uid, ids, context=None):
        res = {}
        sale_order_line_id = self.browse(cr, uid, ids[0], context)
        view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'esc_ventas_ventas', 'desglose_entrega_form')
        view_id = view_ref and view_ref[1] or False
        res = {
            'type': 'ir.actions.act_window',
            'name': 'Desglose de entrega',
            'res_id': sale_order_line_id.id,
            'res_model': 'sale.order.line',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'new'
        }
        return res
    
    # 20/03/2015 (felix) Metodo para guardar desglose de entrega
    def guardar_desglose(self, cr, uid, ids, context=None):
        res = {}
        if ids:
            line_id = self.browse(cr, uid, ids[0], context)['id']
            cant_desglose_ant = 0.00
            src_prods = self.search(cr, uid, [('parent_line_id', '=', line_id)], order='id')
            for i in self.browse(cr, uid, src_prods, context):
                cant_desglose_ant = i.cant_desglose
            if cant_desglose_ant == 0.00:
                cant_desglose_ant = self.browse(cr, uid, ids[0], context)['product_uom_qty']
            cant_desglose = self.browse(cr, uid, ids[0], context)['cant_desglose']
            
            # Verificar que cantidad a entregar no sea mayor o igual a la total restante
            if cant_desglose > cant_desglose_ant:
                raise osv.except_osv('Aviso','La cantidad de desglose es mayor o igual a la cantidad total del producto')
                return {}
                
            restante = cant_desglose_ant - cant_desglose
            res = {
                'product_id': self.browse(cr, uid, ids[0], context)['product_id']['id'],
                'name': self.browse(cr, uid, ids[0], context)['name'],
                'cod_name_prod': self.browse(cr, uid, ids[0], context)['cod_name_prod'],
                'fecha_entrega': self.browse(cr, uid, ids[0], context)['fecha_entrega'],
                'product_uos_qty': cant_desglose,
                'product_uom_qty': cant_desglose,
                'price_unit': self.browse(cr, uid, ids[0], context)['price_unit'],
                'cant_desglose': restante,
                'product_uom': self.browse(cr, uid, ids[0], context)['product_uom']['id'],
                'company_id': self.browse(cr, uid, ids[0], context)['company_id']['id'],
                'order_partner_id': self.browse(cr, uid, ids[0], context)['order_partner_id']['id'],
                'state': 'confirmed',
                'order_id': self.browse(cr, uid, ids[0], context)['order_id']['id'],
                'parent_line_id': self.browse(cr, uid, ids[0], context)['id'],
                'product_desglose': True
            }
            
            # Actualizar remanente de desglose
            res_order_line = {'cant_desglose': restante, 'product_uos_qty': restante, 'product_uom_qty': restante}
            parent_line_id = self.browse(cr, uid, ids[0], context)['id']
            self.write(cr, uid, parent_line_id, res_order_line, context)
            
            # Crear linea de desglose
            prod_line_id = self.create(cr, uid, res, context=context)
            
            # Asociar y actualizar con la salida de almacen
            sale_order_name = self.browse(cr, uid, ids[0], context)['order_id']['name']
            product_id = self.browse(cr, uid, ids[0], context)['product_id']['id']
            obj_stock_move = self.pool.get('stock.move')
            src_stock_move = obj_stock_move.search(cr, uid, [('origin', '=', sale_order_name),('product_id', '=', product_id)])
            get_stock_move = obj_stock_move.browse(cr, uid, src_stock_move[0], context)            
            res_stock_move = {
                'product_id': self.browse(cr, uid, ids[0], context)['product_id']['id'],
                'name': self.browse(cr, uid, ids[0], context)['name'],
                'company_id': get_stock_move['company_id']['id'],
                'state': 'confirmed',
                'product_uos_qty': cant_desglose,
                'product_qty': cant_desglose,
                'product_uom': self.browse(cr, uid, ids[0], context)['product_uom']['id'],
                'product_uos': self.browse(cr, uid, ids[0], context)['product_uom']['id'],
                'partner_id': get_stock_move['partner_id']['id'],
                'parent_line_id': get_stock_move['id'],
                'product_desglose': True,
                'location_dest_id': get_stock_move['location_dest_id']['id'],
                'picking_id': get_stock_move['picking_id']['id'],
                'location_id': get_stock_move['location_id']['id'],
                'fecha_fabricacion': get_stock_move['fecha_fabricacion'],
                'fecha_retest': get_stock_move['fecha_retest'],
                'fecha_caducidad': get_stock_move['fecha_caducidad'],
                'date_expected': self.browse(cr, uid, ids[0], context)['fecha_entrega'],
                'priority': '1',
                'sale_line_id': prod_line_id
            }
            obj_stock_move.create(cr, uid, res_stock_move, context)
            obj_stock_move.write(cr, uid, [get_stock_move['id']], {'product_qty':restante, 'product_uos_qty':restante}, context)
            
            # Generar retorno a la vista de Ventas / Pedidos de ventas
            vista_venta = {}
            sale_order_line_id = self.browse(cr, uid, ids[0], context)
            view_ref = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'esc_ventas_ventas', 'sale_order_form_inherit_2')
            view_id = view_ref and view_ref[1] or False
            vista_venta = {
                'type': 'ir.actions.act_window',
                'name': 'Pedidos de ventas',
                'res_id': sale_order_line_id.order_id.id,
                'res_model': 'sale.order',
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': view_id
            }
                
        return vista_venta

sale_order_line_esc()
