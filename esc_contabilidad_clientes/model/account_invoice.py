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
import logging
_logger = logging.getLogger(__name__)


class account_invoice_line_esc(osv.Model):

    _inherit = 'account.invoice.line'
    _description = 'Cambios y desarrollos para modulo de Contabilidad'
    _columns = {
        'cod_name_prod': fields.char('Codigo y nombre del producto'),
        'caducidad_min': fields.char('Caducidad minima'),
        'condicion': fields.char('Condicion entrega'),
        'especificacion': fields.char('Especificacion')
    }
    
    # 17/03/2015 (felix) Modificacion metodo original para agregar campo "Codigo y nombre del producto" segun el cliente
    def product_id_change(self, cr, uid, ids, product, uom_id, qty=0, name='', type='out_invoice', partner_id=False, fposition_id=False, price_unit=False, currency_id=False, context=None, company_id=None):
        if context is None:
            context = {}
        company_id = company_id if company_id != None else context.get('company_id',False)
        context = dict(context)
        context.update({'company_id': company_id, 'force_company': company_id})
        if not partner_id:
            raise osv.except_osv(_('No Partner Defined!'),_("You must first select a partner!") )
        if not product:
            if type in ('in_invoice', 'in_refund'):
                return {'value': {}, 'domain':{'product_uom':[]}}
            else:
                return {'value': {'price_unit': 0.0}, 'domain':{'product_uom':[]}}
        part = self.pool.get('res.partner').browse(cr, uid, partner_id, context=context)
        fpos_obj = self.pool.get('account.fiscal.position')
        fpos = fposition_id and fpos_obj.browse(cr, uid, fposition_id, context=context) or False

        if part.lang:
            context.update({'lang': part.lang})
        result = {}
        res = self.pool.get('product.product').browse(cr, uid, product, context=context)

        if type in ('out_invoice','out_refund'):
            a = res.property_account_income.id
            if not a:
                a = res.categ_id.property_account_income_categ.id
        else:
            a = res.property_account_expense.id
            if not a:
                a = res.categ_id.property_account_expense_categ.id
        a = fpos_obj.map_account(cr, uid, fpos, a)
        if a:
            result['account_id'] = a

        if type in ('out_invoice', 'out_refund'):
            taxes = res.taxes_id and res.taxes_id or (a and self.pool.get('account.account').browse(cr, uid, a, context=context).tax_ids or False)
        else:
            taxes = res.supplier_taxes_id and res.supplier_taxes_id or (a and self.pool.get('account.account').browse(cr, uid, a, context=context).tax_ids or False)
        tax_id = fpos_obj.map_tax(cr, uid, fpos, taxes)

        if type in ('in_invoice', 'in_refund'):
            result.update( {'price_unit': price_unit or res.standard_price,'invoice_line_tax_id': tax_id} )
        else:
            result.update({'price_unit': res.list_price, 'invoice_line_tax_id': tax_id})
        result['name'] = res.partner_ref

        result['uos_id'] = uom_id or res.uom_id.id
        if res.description:
            result['name'] += '\n'+res.description

        domain = {'uos_id':[('category_id','=',res.uom_id.category_id.id)]}

        res_final = {'value':result, 'domain':domain}

        if not company_id or not currency_id:
            return res_final

        company = self.pool.get('res.company').browse(cr, uid, company_id, context=context)
        currency = self.pool.get('res.currency').browse(cr, uid, currency_id, context=context)

        if company.currency_id.id != currency.id:
            if type in ('in_invoice', 'in_refund'):
                res_final['value']['price_unit'] = res.standard_price
            new_price = res_final['value']['price_unit'] * currency.rate
            res_final['value']['price_unit'] = new_price

        if result['uos_id'] and result['uos_id'] != res.uom_id.id:
            selected_uom = self.pool.get('product.uom').browse(cr, uid, result['uos_id'], context=context)
            new_price = self.pool.get('product.uom')._compute_price(cr, uid, res.uom_id.id, res_final['value']['price_unit'], result['uos_id'])
            res_final['value']['price_unit'] = new_price
            
        # 17/03/2015 (felix) Captura el producto y verifica codigo y nombre segun el cliente
        if partner_id and product:
            obj_product_cliente = self.pool.get('product.cliente')
            src_product_cliente = obj_product_cliente.search(cr, uid, [('cliente_id', '=', partner_id),('producto_cliente_id','=',product)])
            res_final['value']['cod_name_prod'] = ''
            res_final['value']['caducidad_min'] = ''
            res_final['value']['condicion'] = ''
            res_final['value']['especificacion'] = ''
            if src_product_cliente:
                for i in obj_product_cliente.browse(cr, uid, src_product_cliente, context):
                    if i.codigo_prod and i.name:
                        res_final['value']['cod_name_prod'] = '['+str(i.codigo_prod)+'] '+str(i.name)
                    if i.caducidad_id.name and i.caducidad_id.unidad_cad_id.name:
                        res_final['value']['caducidad_min'] = i.caducidad_id.name+' '+i.caducidad_id.unidad_cad_id.name
                    if i.cond_entrega:
                        res_final['value']['condicion'] = i.cond_entrega
                    if i.especificacion:
                        res_final['value']['especificacion'] = i.especificacion
            if not res_final['value']['cod_name_prod']:
                raise osv.except_osv('Aviso','No existe codigo y nombre del producto definido por el cliente.\nDebe crearse el registro en:\nAlmacen/Productos/Productos/Datos del producto por cliente')
            
        return res_final

account_invoice_line_esc()
