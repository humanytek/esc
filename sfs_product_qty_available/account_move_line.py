# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2014 SF Soluciones.
#    (http://www.sfsoluciones.com)
#    contacto@sfsoluciones.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv, orm
import openerp.addons.decimal_precision as dp

class account_move_line(osv.osv):
    _inherit = "account.move.line"
    
    def _compute_balance(self, cr, uid, ids, name, args, context=None):
        res = {}
        
        for line in self.browse(cr, uid, ids, context=context):
            balance = 0.00
            if line.reconcile_id:
                for payment_line in line.reconcile_id.line_id:
                    balance += (payment_line.debit - payment_line.credit)
            elif line.reconcile_partial_id:
                for payment_line in line.reconcile_partial_id.line_partial_ids:
                    balance += (payment_line.debit - payment_line.credit)
            res[line.id] = balance
        return res
    
    def _get_line_from_reconcile(self, cr, uid, ids, context=None):
        result = {}
        for r in self.pool.get('account.move.reconcile').browse(cr, uid, ids, context=context):
            for line in r.line_partial_ids:
                result[line.id] = True
            for line in r.line_id:
                result[line.id] = True
        return result.keys()
    
    _columns = {
        'tot_balance':fields.function(_compute_balance, digits_compute=dp.get_precision('Account'), string='Balance',
                                   type='float', store={
                'account.move.line': (lambda self, cr, uid, ids, c={}: ids, ['debit','credit','reconcile_id','reconcile_partial_id'], 20),
                'account.move.reconcile': (_get_line_from_reconcile, None, 20),
                
            },
            ),
                
    }
account_move_line()





# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
