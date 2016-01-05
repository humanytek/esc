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
    
    # 22/12/2015 (felix) Metodo para obtener valores del producto segun el cliente
    def _get_prod_cli(self, cr, uid, ids, field_name, args, context=None):
        res = {}
        for i in self.browse(cr, uid, ids, context):
            res[i.id] = 0
            obj_prod_cliente = self.pool.get('product.cliente')
            src_prod_cliente = obj_prod_cliente.search(cr, uid, [('producto_cliente_id', '=', i.product_id.id), ('cliente_id', '=', i.partner_id.id)])
            if src_prod_cliente:
                res[i.id] = obj_prod_cliente.browse(cr, uid, src_prod_cliente[0], context).id
        return res
        
    # 22/12/2015 (felix) Metodo para obtener valores de pedimento
    def _get_pedimento(self, cr, uid, ids, field_name, args, context=None):
        res = {}
        _logger.warn('Entra al metodo')
        for i in self.browse(cr, uid, ids, context):
            _logger.warn('Entra al for')
            res[i.id] = 0
            """
            obj_account_invoice_rel = self.pool.get('account.invoice.rel')
            src_account_invoice_rel = obj_account_invoice_rel.search(cr, uid, [('invoice_id', '=', i.invoice_id.id)])
            _logger.warn('Valor de invoice_rel %s', src_account_invoice_rel)
            if src_account_invoice_rel:
                import_id = obj_account_invoice_rel.browse(cr, uid, src_account_invoice_rel[0], context).import_id
                obj_pedimento = self.pool.get('import.info')
                src_pedimento = obj_pedimento.search(cr, uid, ['id', '=', import_id])
                if src_pedimento:
                    res[i.id] = obj_pedimento.browse(cr, uid, src_pedimento[0], context).id
                    _logger.warn('Valor de valor %s', res)
            """
        return res
    
    _columns = {
        'prod_cli_id': fields.function(_get_prod_cli, type='many2one', 
            obj='product.cliente', string='Producto cliente'),
        'pedimento_id': fields.function(_get_pedimento, type='many2one',
            obj='import.info', string='Pedimento')
    }

account_invoice_line_esc()
