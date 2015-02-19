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

from osv import osv

import time
from tools.translate import _

class sale_order(osv.osv):
    _inherit = 'sale.order'
    
    def check_limit(self, cr, uid, ids, context=None):
        for so in self.browse(cr, uid, ids, context=context):
            partner = so.partner_id
            moveline_obj = self.pool.get('account.move.line')
            movelines = moveline_obj.search(cr, uid, [('partner_id', '=', partner.id),('account_id.type', 'in', ['receivable', 'payable']), ('state', '<>', 'draft'), ('reconcile_id', '=', False)])
            movelines = moveline_obj.browse(cr, uid, movelines)
            debit, credit = 0.0, 0.0
            debit_maturity, credit_maturity = 0.0, 0.0
            for line in movelines:
                if line.date_maturity < time.strftime('%Y-%m-%d') and line.date_maturity <> False:
                    credit_maturity += line.debit
                    debit_maturity += line.credit
                credit += line.debit
                debit += line.credit
            saldo = credit - debit
            saldo_maturity = credit_maturity - debit_maturity
            if not partner.over_credit:
                if (saldo + so.amount_total) > partner.credit_limit and partner.credit_limit > 0.00:
                    msg = _('Can not validate the Sale Order because it has exceeded the credit limit \nCredit Amount: %s\nCredit Limit: %s \nCheck the credit limits on Partner')%(saldo + so.amount_total, partner.credit_limit)
                    raise osv.except_osv(_('Credit Over Limits !'), (msg))
                    return False
            if not partner.maturity_over_credit:
                if (saldo_maturity) > partner.credit_maturity_limit and partner.credit_maturity_limit > 0.00:
                    msg = _('Can not validate the Sale Order because it has exceeded the credit limit up to date: %s \nMaturity Amount: %s \nMaturity Credit Limit: %s \nCheck the credit limits on Partner')%(time.strftime('%Y-%m-%d'), saldo_maturity, partner.credit_maturity_limit)
                    raise osv.except_osv(_('Maturity Credit Over Limits !'), (msg))
                    return False
        return True

sale_order()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
