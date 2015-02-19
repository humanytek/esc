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
from openerp.osv import fields, osv

class product_product(osv.osv):
    _inherit = 'product.product'
    def default_get(self, cr, uid, fields, context=None):
        if context is None:
            context = {}
        res = super(product_product, self).default_get(cr, uid, fields, context=context)
        default_code = self.pool.get('ir.sequence').get(cr, uid, 'product.product') or ''
        res.update({'default_code' : default_code})
        return res
#     def create(self, cr, uid, vals, context=None):
#         if not vals.get('default_code', False):
#             vals['default_code'] = self.pool.get('ir.sequence').get(cr, uid, 'product.product') or ''
#         return super(product_product, self).create(cr, uid, vals, context=context)
    def _group_manager(self, cr, uid, ids, field_name, arg, context={}):
        res = {}
        manager_group_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'hmtk_esic_product_info', 'group_product_attributes_manager')[1]
        manager_group = self.pool.get('res.groups').browse(cr, uid, manager_group_id, context=context)
        manager_user_ids = [x.id for x in manager_group.users]
        for id in ids:
            if uid in manager_user_ids:
                res[id] = True
            else:
                res[id] = False
        return res
    def _group_user(self, cr, uid, ids, field_name, arg, context={}):
        res = {}
        user_group_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'hmtk_esic_product_info', 'group_product_attributes_user')[1]
        user_group = self.pool.get('res.groups').browse(cr, uid, user_group_id, context=context)
        user_user_ids = [x.id for x in user_group.users]
        for id in ids:
            if uid in user_user_ids:
                res[id] = True
            else:
                res[id] = False
        return res
    
        

    _columns = {
        'cas_no': fields.char('CAS Number', size=32, help='Entering CAS number'),
        'previous_no':  fields.char('Previous Number', size=32),
        'product_attribute_ids': fields.one2many('product.attribute', 'product_id', 'Product Attributes'),
        'tarrif_fraction_ids': fields.one2many('product.tarrif_fraction', 'product_id', 'Tarrif Fraction'),
        'document_ids': fields.one2many('product.document', 'product_id', 'Documents'),
        'group_manager': fields.function(_group_manager, type="boolean", string="Manager"),
        'group_user': fields.function(_group_user, type="boolean", string="User"),
        }
    
product_product()

class product_attribute(osv.osv):
    _name = 'product.attribute'
    _columns = {
        'name': fields.char('Attribute', size=32, required=True),
        'product_id': fields.many2one('product.product', 'Product')
        }
product_attribute()

class product_tarrif_fraction(osv.osv):
    _name = 'product.tarrif_fraction'
    _columns = {
        'name': fields.char('Tarrif Fraction', size=32, required=True),
        'product_id': fields.many2one('product.product', 'Product')
        }
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Tarrif fraction must be unique'),
    ]
product_tarrif_fraction()

class product_document(osv.osv):
    _name = 'product.document'
    _columns = {
        'name': fields.char('Document Name', size=32, required=True),
        'document': fields.binary('Document'),
        'product_id': fields.many2one('product.product', 'Product'),
        }
product_document()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: