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

from osv import osv, fields

import openerp.addons.decimal_precision as dp

class user_transaction_history(osv.osv):
    _name = 'user.transaction.history'
    _description = 'Model to keep record of user payments and refund'
    _rec_name = 'transaction_date'
    
    def _get_history(self, cr, uid, ids, context=None):
        move_line_pool = self.pool.get('account.move.line')
        history_pool = self.pool.get('user.transaction.history')
        history_ids = history_pool.search(cr, uid, [('move_line_id', 'in', ids)], context=context)
        return history_ids
    
    def _get_voucher_history(self, cr, uid, ids, context=None):
        voucher_pool = self.pool.get('account.voucher')
        history_pool = self.pool.get('user.transaction.history')
        history_ids = history_pool.search(cr, uid, [('payment_id', 'in', ids)], context=context)
        return history_ids
    
    def _get_transaction_date(self, cr, uid, ids, name, args, context=None):
        res = {}
        for history_obj in self.browse(cr, uid, ids, context=context):
            if history_obj.payment_id:
                res[history_obj.id] = history_obj.payment_id.date
            else:
                res[history_obj.id] = history_obj.move_line_id.date
        return res
    
    _columns = {
                'user_id': fields.many2one('res.users', 'User'),
                'transaction_date': fields.function(_get_transaction_date, type="date", string="Transaction Date",
                                                    store={
                                                           'account.move.line': (_get_history, ['date'], 10),
                                                           'account.voucher': (_get_voucher_history, ['date'], 10),
                                                           'user.transaction.history' : (lambda self, cr, uid, ids, c={}: ids, [], 5),
                                                           }),
                'transaction_type': fields.selection([('payment', 'Payment'), ('refund', 'Refund')],
                                                     'Transaction Type'),
                'invoice_id': fields.many2one('account.invoice', 'Related Invoice'),
                'payment_id': fields.many2one('account.voucher', 'Related Payment'),
                'move_line_id': fields.many2one('account.move.line', 'Related Journal Item'),
                'amount': fields.float('Amount', digits_compute=dp.get_precision('Account'))
                }
user_transaction_history()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
