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
class stock_move(osv.osv):
    _inherit = 'stock.move'
    _columns = {
        'certificate_id': fields.many2one('product.import.certificate', 'Product Import Certificate'),
        'import_certificate': fields.boolean('Import_Certificate'),
        }
    def onchange_product_id(self, cr, uid, ids, prod_id=False, loc_id=False,
                            loc_dest_id=False, partner_id=False):
        value = super(stock_move, self).onchange_product_id(cr, uid, ids, prod_id, loc_id, loc_dest_id, partner_id)
        import_certificate = False
        product = self.pool.get('product.product').browse(cr, uid, prod_id)
        if product.import_certificate:
            import_certificate = True
        result = value['value']
        result.update({'import_certificate' : import_certificate})
        value.update({'value': result})
        return value
stock_move()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: