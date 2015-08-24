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


class product_import_certificate_line_esc(osv.Model):

    _name = 'product.import.certificate.line'
    _description = 'Creacion modelo Certificados de analisis'
    _columns = {
        'name': fields.char('Pais', size=250),
        'cod_pais': fields.char('Codigo de pais', size=250),
        'moneda_id': fields.many2one('res.currency', 'Moneda'),
        'certificado_id': fields.many2one('product.import.certificate',
            'Certificado de importacion')
    }
    
product_import_certificate_line_esc()


class product_import_certificate_esc(osv.Model):

    _inherit = 'product.import.certificate'
    _description = 'Datos adicionales de permisos de importacion'
    
    # 17/06/2015 (felix) Metodo de los hindues, daba un error
    def unlink(self, cr, uid, ids, context=None):
        for i in self.browse(cr, uid, ids, context=context):
            if i.state != 'new':
                if i.state == 'not_extend':
                    raise osv.except_osv(_('Warning!'), _('You cannot do any operation in the record which is not extendable.'))
                else:
                    raise osv.except_osv(_('Warning!'), _('For deleting the record, the state should be in New.'))
        return super(product_import_certificate_esc, self).unlink(cr, uid, ids, context=context)
    
    # 17/06/2015 (felix) Metodo de los hindues, daba un error
    def change_state(self, cr, uid, ids,context=None):
        for i in self.browse(cr, uid, ids, context=context):
            if i.state == 'new':
                self.write(cr, uid, [i.id], {'state': 'active'}, context=context)
            if i.state == 'active':
                self.write(cr, uid, [i.id], {'state': 'in_renov'}, context=context)
            if i.state == 'in_renov':
                self.write(cr, uid, [i.id], {'state': 'renov', 'renewable': True,}, context=context)
            if i.state == 'renov':
                self.write(cr, uid, [i.id], {'state': 'spent'}, context=context)
            if i.state == 'spent':
                self.write(cr, uid, [i.id], {'state': 'not_extend'}, context=context)
        return True
    
    # 17/06/2015 (felix) Metodo de los hindues, daba un error
    def previous_state(self, cr, uid, ids,context=None):
        for i in self.browse(cr, uid, ids, context=context):
            if i.state == 'active':
                self.write(cr, uid, [i.id], {'state': 'new'}, context=context)
            if i.state == 'in_renov':
                self.write(cr, uid, [i.id], {'state': 'active'}, context=context)
            if i.state == 'renov':
                self.write(cr, uid, [i.id], {'state': 'in_renov'}, context=context)
            if i.state == 'spent':
                self.write(cr, uid, [i.id], {'state': 'renov'}, context=context)
        return True
    
    # 17/06/2015 (felix) Metodo de los hindues, daba un error
    def _calculate_days(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        diff_days = 0
        for i in self.browse(cr, uid, ids, context=context):
            res[i.id] = 0
            if i.end_term and i.initial_term:
                diff_days = datetime.strptime(i.end_term, '%Y-%m-%d')-datetime.strptime(i.initial_term, '%Y-%m-%d')
                diff_days = diff_days.days
            res[i.id] = diff_days
        return res
    
    # 17/06/2015 (felix) Metodo de los hindues, daba un error
    def _calculate_stock_qty(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        move_pool = self.pool.get('stock.move')
        stock_qty = 0.00
        for i in self.browse(cr, uid, ids, context=context):
            res[i.id] = 0.00
            move_lines = move_pool.search(cr, uid, [('certificate_id', '=', i.id)],  context=context)
            if move_lines:
                stock_qty = sum([move.product_qty for move in move_pool.browse(cr, uid, move_lines)])
                qty = i.qty
                stock_qty = stock_qty
            res[i.id] = stock_qty
        return res
    
    # 17/06/2015 (felix) Metodo de los hindues, daba un error
    def _calculate_qty(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        move_pool = self.pool.get('stock.move')
        qty_imported = 0
        for i in self.browse(cr, uid, ids, context=context):
            res[i.id] = 0.00
            move_lines = move_pool.search(cr, uid, [('certificate_id', '=', i.id)],  context=context)
            if move_lines:
                stock_qty = sum([move.product_qty for move in move_pool.browse(cr, uid, move_lines)])
                qty = i.qty
                qty_imported = qty - stock_qty
            else:
                qty_imported = i.qty
            res[i.id] = qty_imported
        return res
    
    # 17/06/2015 (felix) Metodo de los hindues, daba un error
    def _line_state(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for i in self.browse(cr, uid, ids, context=context):
            res[i.id] = ''
            if i.diff_days < 60 and i.diff_days >= 45:
                res[i.id] = 'blue'
            elif i.diff_days < 45:
                res[i.id] = 'red'
        return res
        
    # 17/06/2015 (felix) Metodo de los hindues, daba un error
    def _qty_uom(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        qty_uom = ''
        for i in self.browse(cr, uid, ids, context=context):
            res[i.id] = ''
            if i.uom_id and i.qty:
                qty_uom = str(i.qty)+' / '+str(i.uom_id.name)
            res[i.id] = qty_uom
        return res
        
    # 20/08/2015 (felix) Captura de datos para lista de productos por numero de permiso de importacion
    """
    def _get_move_in(self, cr, uid, ids, field_name, arg=None, context=None):
        res = {}
        if not ids:
            return res
        for i in ids:
            result.setdefault(i, [])
        cr.execute('''SELECT WHERE certificate_number
        ''')
        res_q = cr.fetchall()
        for r in res_q:
            res[r[0]].append(r[1])
        return res
    """
    
    _columns = {
        'background_country_ids': fields.one2many('product.import.certificate.line', 
            'certificado_id', 'Backgrounds'),
    }
    _rec_name = 'certificate_number'
    
product_import_certificate_esc()
