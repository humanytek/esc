# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-2014 ZestyBeanz Technologies Pvt Ltd(<http://www.zbeanztech.com>).
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
from osv import fields, osv
from datetime import datetime
from openerp.tools.translate import _
class product_import_certificate(osv.osv):
    _name = 'product.import.certificate'
    _inherit = ['mail.thread']
    _rec_name = 'certificate_number'
    
    def _get_cer_no(self, cr, uid, ids, context=None):
        cer_seq = self.pool.get('ir.sequence').get(cr, uid, 'product.import.certificate')
        return cer_seq
    
    def unlink(self, cr, uid, ids, context=None):
        for id in ids:
            certificate = self.browse(cr, uid, id, context=context)
            if certificate.state != 'new':
                if certificate.state == 'not_extend':
                    raise osv.except_osv(_('Warning!'), _('You cannot do any operation in the record which is not extendable.'))
                else:
                    raise osv.except_osv(_('Warning!'), _('For deleting the record, the state should be in New.'))
        return super(product_import_certificate, self).unlink(cr, uid, ids, context=context)
    
    def copy(self, cr, uid, ids, default=None, context=None):
        if default is None:
            default = {}
        default = default.copy()
        default['certificate_number'] = self._get_cer_no(cr, uid, ids, context)
        default['qty'] = 0.0
#         default['move_id'] = False
        return super(product_import_certificate, self).copy(cr, uid, ids, default, context=context)
    
    def create(self, cr, uid, vals, context=None):
        stock_move_pool = self.pool.get('stock.move')
        product_pool = self.pool.get('product.product')
        product_name = product_pool.browse(cr, uid, vals['product_id'], context=context).name
        vals['name'] = product_name
        return super(product_import_certificate, self).create(cr, uid, vals, context=context)
    
    def write(self, cr, uid, ids, vals, context=None):
        stock_move_pool = self.pool.get('stock.move')
        for id in ids:
            certificate = self.browse(cr, uid, id, context=context)
            if 'qty' in vals:
                move_qty = certificate.move_qty
                total = vals['qty'] - move_qty 
                if total <= 0:
                    vals['state'] = 'spent'
        return super(product_import_certificate, self).write(cr, uid, ids, vals, context=context)    
    
    def change_state(self, cr, uid, ids,context=None):
        for id in ids:
            certificate = self.browse(cr, uid, id, context=context)
            if certificate.state == 'new':
                self.write(cr, uid, [id], {'state': 'active'}, context=context)
            if certificate.state == 'active':
                self.write(cr, uid, [id], {'state': 'in_renov'}, context=context)
            if certificate.state == 'in_renov':
                self.write(cr, uid, [id], {'state': 'renov', 'renewable': True,}, context=context)
            if certificate.state == 'renov':
                self.write(cr, uid, [id], {'state': 'spent'}, context=context)
            if certificate.state == 'spent':
                self.write(cr, uid, [id], {'state': 'not_extend'}, context=context)
        return True
    
    def previous_state(self, cr, uid, ids,context=None):
        for id in ids:
            certificate = self.browse(cr, uid, id, context=context)
            if certificate.state == 'active':
                self.write(cr, uid, [id], {'state': 'new'}, context=context)
            if certificate.state == 'in_renov':
                self.write(cr, uid, [id], {'state': 'active'}, context=context)
            if certificate.state == 'renov':
                self.write(cr, uid, [id], {'state': 'in_renov'}, context=context)
            if certificate.state == 'spent':
                self.write(cr, uid, [id], {'state': 'renov'}, context=context)
        return True
    
    def _calculate_days(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        diff_days = 0
        for id in ids:
            obj = self.browse(cr, uid, id, context=context)
            if obj.end_term and obj.initial_term:
                diff_days = datetime.strptime(obj.end_term, '%Y-%m-%d')-datetime.strptime(obj.initial_term, '%Y-%m-%d')
                diff_days = diff_days.days
            res[id] = diff_days
        return res
    
    def _calculate_stock_qty(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        move_pool = self.pool.get('stock.move')
        stock_qty = 0
        for id in ids:
            obj = self.browse(cr, uid, id, context=context)
            move_lines = move_pool.search(cr, uid, [('certificate_id', '=', obj.id)],  context=context)
            if move_lines:
                stock_qty = sum([move.product_qty for move in move_pool.browse(cr, uid, move_lines)])
                qty = obj.qty
                stock_qty = stock_qty
            res[id] = stock_qty
        return res
    
    def _calculate_qty(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        move_pool = self.pool.get('stock.move')
        qty_imported = 0
        for id in ids:
            obj = self.browse(cr, uid, id, context=context)
            move_lines = move_pool.search(cr, uid, [('certificate_id', '=', obj.id)],  context=context)
            if move_lines:
                stock_qty = sum([move.product_qty for move in move_pool.browse(cr, uid, move_lines)])
                qty = obj.qty
                qty_imported = qty - stock_qty
            else:
                qty_imported = obj.qty
            res[id] = qty_imported
        return res
    
    def _line_state(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for id in ids:
            obj = self.browse(cr, uid, id, context=context)
            if obj.diff_days < 60 and obj.diff_days >= 45:
                res[id] = 'blue'
            elif obj.diff_days < 45:
                res[id] = 'red'
        return res
    
    def _qty_uom(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        qty_uom = ''
        for id in ids:
            obj = self.browse(cr, uid, id, context=context)
            if obj.uom_id and obj.qty:
                qty_uom = str(obj.qty)+' / '+str(obj.uom_id.name)
            res[id] = qty_uom
        return res
    
    _columns = {
        'state': fields.selection([('new', 'New'), ('active', 'Active'),
                                   ('in_renov', 'In Renovation'), ('renov', 'Renovated'),
                                   ('spent', 'Spent'), ('not_extend', 'Not Extendable')], 'Status',  track_visibility='onchange'), 
        'certificate_number': fields.char('Certificate Number', size=64, states={'not_extend':[('readonly',True)]}, required=True),
        'certificate_date': fields.date('Date of Certificate', states={'not_extend':[('readonly',True)]}, required=True, track_visibility='onchange'),
        'initial_term': fields.date('Initial Term', states={'not_extend':[('readonly',True)]}, track_visibility='onchange'), 
        'end_term': fields.date('End Term', states={'not_extend':[('readonly',True)]}, track_visibility='onchange'),
        'renewable': fields.boolean('Renewable', states={'not_extend':[('readonly',True)]}, track_visibility='onchange'),
        'manufacturer_id': fields.many2one('res.partner', 'Manufacturer', states={'not_extend':[('readonly',True)]}),
        'custom': fields.many2one('import.info.custom', 'Custom', states={'not_extend':[('readonly',True)]}),
        'source': fields.many2one('res.country', 'Source', states={'not_extend':[('readonly',True)]}),
        'raw_material_imported': fields.char('Raw material to be imported', size=64, states={'not_extend':[('readonly',True)]}), 
        'product_id': fields.many2one('product.product', 'Product', required=True, states={'not_extend':[('readonly',True)]}),
        'import_certificate': fields.boolean('Import_Certificate', states={'not_extend':[('readonly',True)]}),
        'qty': fields.float('Quantity', states={'not_extend':[('readonly',True)]}), 
        'uom_id':  fields.many2one('product.uom', 'UOM', states={'not_extend':[('readonly',True)]}),
        'fraction_id': fields.many2one('product.tarrif_fraction', 'Fraction', states={'not_extend':[('readonly',True)]}),
        'qty_uom': fields.function(_qty_uom,  type='char', string='Qtty/UOM', states={'not_extend':[('readonly',True)]}),
#         'move_id': fields.many2one('stock.move', 'Stock Move', states={'not_extend':[('readonly',True)]}),
        'qty_imported': fields.function(_calculate_qty, type='float', string='Quantity Imported', states={'not_extend':[('readonly',True)]}),
        'diff_days':  fields.function(_calculate_days, type='integer', string='Difference', states={'not_extend':[('readonly',True)]}),
        'line_state': fields.function(_line_state, type='selection', string='Line state', selection=[('blue', 'Blue'), ('red', 'Red')]),
        'name': fields.char('Name', size=128, required=True, states={'not_extend':[('readonly',True)]}),
        'notes': fields.text('Notes', states={'not_extend':[('readonly',True)]}),
        'move_qty': fields.function(_calculate_stock_qty, type='float', string='Stock Qty'),
        'background_country_ids': fields.one2many('res.country', 'certificate_id', 'Backgrounds'),
        }
    _defaults = { 
        'line_state': 'blue',
        'state': 'new',
        'certificate_number': _get_cer_no,
        'qty_imported': 0.0
        }
    def onchange_product(self, cr, uid, ids, product_id, context=None):
        res = {}
        product_obj = self.pool.get('product.product')
        if product_id:
            product = product_obj.browse(cr, uid, product_id, context=context)
            uom_id = product.uom_id.id
            if product.import_certificate:
                value = {'import_certificate' : True}
            else:
                value = {'import_certificate' : False}
            if product.manufacturer:
                value.update({'manufacturer_id': product.manufacturer.id})
            
        if uom_id:
            value.update({'uom_id': uom_id})
        res.update({'value': value})
        return res
    
product_import_certificate()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: