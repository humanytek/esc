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

class account_move_line(osv.osv):
    _inherit = 'account.move.line'
    
    def get_voucher_details(self, cr, uid, ids, context=None):
        voucher_pool = self.pool.get('account.voucher')
        for move_line_obj in self.browse(cr, uid, ids, context=context):
            voucher_ids = voucher_pool.search(cr, uid, [('move_id', '=', move_line_obj.move_id.id)], context=context)
            if voucher_ids:
                return voucher_ids[0]
        return False
    
    def create_trans_history(self, cr, uid, ids, context=None):
        reconcile_payment_dict = {}
        move_line_pool = self.pool.get('account.move.line')
        voucher_pool = self.pool.get('account.voucher')
        user_transaction_history_pool = self.pool.get('user.transaction.history')
        for move_line_obj in self.browse(cr, uid, ids, context=context):
            if move_line_obj.invoice and move_line_obj.invoice.type in ['out_invoice', 'out_refund']:
                invoice_type = move_line_obj.invoice.type
                reconcile_obj = move_line_obj.reconcile_id or move_line_obj.reconcile_partial_id or False
                if not reconcile_payment_dict.get(reconcile_obj.id, False):
                    reconcile_payment_dict[reconcile_obj.id] = self.get_voucher_details(cr, uid, ids, context=context)
                voucher_id = reconcile_payment_dict.get(reconcile_obj.id, False)
                partner_obj = move_line_obj.partner_id
                domain = ['|', ('reconcile_id', '=', reconcile_obj.id),
                          ('reconcile_partial_id', '=', reconcile_obj.id)]
                amount = move_line_obj.credit or move_line_obj.debit or 0.00
                if invoice_type == 'out_refund':
                    transaction_type = 'refund'
                    partner_account = partner_obj.property_account_payable and \
                                            partner_obj.property_account_payable.id or False
                    domain.append(('debit', '>', 0.00))
                else:
                    transaction_type = 'payment'
                    partner_account = partner_obj.property_account_receivable and \
                                            partner_obj.property_account_receivable.id or False
                    domain.append(('credit', '>', 0.00))
                parent_move_line_ids = move_line_pool.search(cr, uid, domain, context=context)
                split_line = False
                if len(parent_move_line_ids) > 1:
                    split_line = True
                for parent_move_line_obj in move_line_pool.browse(cr, uid, parent_move_line_ids, context=context):
                    if split_line:
                        amount = parent_move_line_obj.credit or parent_move_line_obj.debit or 0.00
                    invoice_id = move_line_obj.invoice and move_line_obj.invoice.refund_invoice_id and \
                                        move_line_obj.invoice.refund_invoice_id.id or \
                                        move_line_obj.invoice.id or False
                    vals = {
                            'user_id': uid,
                            'transaction_type': transaction_type,
                            'payment_id': voucher_id,
                            'invoice_id': invoice_id,
                            'amount': amount,
                            'move_line_id': parent_move_line_ids[0]
                            }
                    history_id = user_transaction_history_pool.create(cr, uid, vals, context=context)
        return True
    
    def reconcile_partial(self, cr, uid, ids, type='auto', context=None, writeoff_acc_id=False,
                          writeoff_period_id=False, writeoff_journal_id=False):
        if context is None:
            context = {}
        context['history_created'] = True
        context['source'] = 'partial'
        res = super(account_move_line, self).reconcile_partial(cr, uid, ids, type, context, writeoff_acc_id,
                                                               writeoff_period_id, writeoff_journal_id)
        self.create_trans_history(cr, uid, ids, context=context)
        return res
    
    def reconcile(self, cr, uid, ids, type='auto', writeoff_acc_id=False, writeoff_period_id=False,
                  writeoff_journal_id=False, context=None):
        if context is None:
            context = {}
        context['source'] = 'full'
        res = super(account_move_line, self).reconcile(cr, uid, ids, type, writeoff_acc_id, writeoff_period_id,
                                                       writeoff_journal_id, context=context)
        if not context.get('history_created', False):
            self.create_trans_history(cr, uid, ids, context=context)
        return True
        
    
account_move_line()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
