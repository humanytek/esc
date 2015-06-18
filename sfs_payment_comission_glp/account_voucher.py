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

from datetime import datetime

class account_voucher(osv.osv):
    _inherit = 'account.voucher'
    
    def cancel_voucher(self, cr, uid, ids, context=None):
        user_tran_history_pool = self.pool.get('user.transaction.history')
        res = super(account_voucher, self).cancel_voucher(cr, uid, ids, context=context)
        user_tran_history_ids = user_tran_history_pool.search(cr, uid, [('payment_id', 'in', ids)],
                                                              context=context)
        user_tran_history_pool.unlink(cr, uid, user_tran_history_ids, context=context)
        return res
    
account_voucher()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
