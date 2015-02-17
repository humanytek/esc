# -*- encoding: utf-8 -*
##############################################################################
#
#    Copyright (c) 2013 SF Soluciones.
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

from sfs_reconcile_ledger_report import JasperDataParser
from jasper_reports import jasper_report
from openerp.tools.translate import _


class jasper_ledger_report(JasperDataParser.JasperDataParser):
    
    def __init__(self, cr, uid, ids, data, context):
        self.move_line_ids = []
        self.reconcile_invoice_dict = {}
        super(jasper_ledger_report, self).__init__(cr, uid, ids, data, context)

    def generate_data_source(self, cr, uid, ids, data, context):
        return 'xml_records'

    def generate_parameters(self, cr, uid, ids, data, context):
        result = {}
        if context is None:
            context = {}
        way = data.get('way', 'debit_to_credit')
        partner_pool = self.pool.get('res.partner')
        fiscal_yr = ''
        if data.get('fiscalyear_id', False):
            fiscal_year = self.pool.get('account.fiscalyear').browse(cr, uid, data['fiscalyear_id'][0], context=context)
            fiscal_yr = fiscal_year and fiscal_year.name or ''
        if data['filter']=='period':
            period_from = self.pool.get('account.period').browse(cr, uid, data['period_from_id'][0], context=context).name
            period_to = self.pool.get('account.period').browse(cr, uid, data['period_to_id'][0], context=context).name
        partner_ids = context.get('active_ids', [])
        partner_list = [x.name for x in partner_pool.browse(cr, uid, partner_ids, context=context) if partner_ids]
        trans = {
                    'date' : _('Date'),
                    'account' : _('Account'),
                    'entry_label' : _('Entry Label'),
                    'ref' : _('Reconcile'),
                    'debit' : _('Debit'),
                    'credit' : _('Credit'),
                    'balance' : _('Balance'),
                    'doc_balance' : _('Document Balance'),
                    'tot_balance': _('Total Balance'),
                    'partner_ledger': _('Reconcile Ledger'),
                    'acc_rec': _('Accounts Receivable'),
                    'fiscal_yr': _('Fiscal Year'),
                    'filter_by': _('Filters By'),
                    'target_move': _('Target Moves'),
                    'document_bal':_('Document Balance'),
                    'targ_move': _('Posted'),
                    'jnl_ref': _('Reference'),
                    'partner': way == 'debit_to_credit' and _('Customer') or _('Supplier'),
                    'fiscal_year': fiscal_yr,
                    'start_period': data['filter']=='period' and _('Start Period') or 
                                                data['filter']=='date' and _('Start Date') or '',
                    'end_period': data['filter']=='period' and _('End Period') or 
                                                data['filter']=='date' and _('End Date') or '',
                     
                    'period_from': data['filter']=='period' and period_from or 
                                               data['filter']=='date' and data['date_from'] or '',
                    'period_to': data['filter']=='period' and period_to or 
                                               data['filter']=='date' and data['date_to'] or '',
                    'company': self.pool.get('res.users').browse(cr, uid, uid,  context=context).company_id.name,
                    'way': data.get('way', 'debit_to_credit'),
                    'partner_name': ','.join(partner_list)
                     }
        result.update(trans)  
        return result
    
    def get_invoice_ids(self, cr, uid, ids, reconcile_id, context=None):
        move_line_pool = self.pool.get('account.move.line')
        invoice_id = False
        if self.reconcile_invoice_dict.get(reconcile_id, False):
            move_line_ids = self.reconcile_invoice_dict[reconcile_id]
        else:
            move_line_ids = move_line_pool.search(cr, uid, ['|', ('reconcile_id', '=', reconcile_id),
                                                            ('reconcile_partial_id', '=', reconcile_id),
                                                            ('invoice', '!=', False)], context=context)
            self.reconcile_invoice_dict[reconcile_id] = move_line_ids
        if move_line_ids:
            self.move_line_ids.append(move_line_ids[0])
            move_line_obj = move_line_pool.browse(cr, uid, move_line_ids[0], context=context)
            return move_line_obj.invoice.id
        return False
    
    def generate_records(self, cr, uid, ids, data, context):
        if context is None:
            context = {}
        account_period_pool = self.pool.get('account.period')
        move_line_pool = self.pool.get('account.move.line')
        invoice_pool = self.pool.get('account.invoice')
        wizard_pool = self.pool.get('reconcile.ledger.report')
        result = []
        domain = [('state', '!=', 'draft')]
        way = data.get('way', 'debit_to_credit')
        if data.get('fiscalyear_id', False):
            fiscal_year_id = data['fiscalyear_id'][0]
            fiscal_year_data = wizard_pool.onchange_filter(cr, uid, ids, filter='period', fiscalyear_id=fiscal_year_id,
                                                           context=context)
            start_period_id = fiscal_year_data['value']['period_from_id']
            end_period_id = fiscal_year_data['value']['period_to_id']
            from_period_obj = account_period_pool.browse(cr, uid, start_period_id, context=context)
            to_period_obj = account_period_pool.browse(cr, uid, end_period_id, context=context)
            date_from = from_period_obj.date_start
            date_to = to_period_obj.date_stop
            domain.extend([('date', '>=', date_from), ('date', '<=', date_to)])
        if way == 'debit_to_credit':
            domain.append(('account_id.type', '=', 'receivable'))
        else:
            domain.append(('account_id.type', '=', 'payable'))
        if data.get('filter', 'none') == 'date':
            date_from = data['date_from']
            date_to = data['date_to']
            domain.extend([('date', '>=', date_from), ('date', '<=', date_to)])
        if data.get('filter', 'none') == 'period':
            from_period_id = data['period_from_id'][0]
            to_period_id = data['period_to_id'][0]
            from_period_obj = account_period_pool.browse(cr, uid, from_period_id, context=context)
            to_period_obj = account_period_pool.browse(cr, uid, to_period_id, context=context)
            date_from = from_period_obj.date_start
            date_to = to_period_obj.date_stop
            domain.extend([('date', '>=', date_from), ('date', '<=', date_to)])
        if context.get('active_ids', False):
            domain.append(('partner_id', 'in', context['active_ids']))
        if data.get('journal_ids', []):
            domain.append(('journal_id', 'in', data['journal_ids']))
        move_line_ids = move_line_pool.search(cr, uid, domain, context=context)
        for move_line_obj in move_line_pool.browse(cr, uid, move_line_ids, context=context):
            reconcile_obj = move_line_obj.reconcile_id or move_line_obj.reconcile_partial_id or False
            invoice_type = 'out_invoice'
            invoice_id = False
            if not move_line_obj.invoice and reconcile_obj:
                invoice_id = self.get_invoice_ids(cr, uid, ids, reconcile_obj.id, context=context)
            else:
                invoice_id = move_line_obj.invoice.id or False
            if invoice_id:
                invoice_obj = invoice_pool.browse(cr, uid, invoice_id, context=context)
                invoice_type = invoice_obj.type
                if invoice_type in ['out_refund', 'in_refund']:
                    invoice_id = invoice_obj.refund_invoice_id and invoice_obj.refund_invoice_id.id or \
                                    False
            currency = move_line_obj.currency_id or move_line_obj.company_id.currency_id
            amount = move_line_obj.amount_currency if currency != move_line_obj.company_id.currency_id else \
                                move_line_obj.debit - move_line_obj.credit
            credit = '0.00'
            debit = '0.00'
            if invoice_type == 'out_invoice' and amount > 0:
                debit = amount
            elif invoice_type == 'in_invoice' and amount > 0:
                credit = amount
            elif invoice_type == 'out_invoice' and amount < 0:
                credit = amount * -1
            elif invoice_type == 'in_invoice' and amount < 0:
                debit = amount * -1
            elif invoice_type in ['out_refund', 'in_refund']:
                credit = amount * -1
            data = {
                    'date': move_line_obj.date,
                    'journal': move_line_obj.journal_id and \
                                     move_line_obj.journal_id.name or '',
                    'account': move_line_obj.account_id.code + " " + move_line_obj.account_id.name or "",
                    'name': move_line_obj.name or '',
                    'debit': debit,
                    'credit': credit,
                    'reconcile': reconcile_obj and reconcile_obj.name or '',
                    'invoice_id': invoice_id,
                    'ref': move_line_obj.ref
                    }
            result.append(data)
            if way == 'debit_to_credit':
                result = sorted(result, key = lambda d: (d['invoice_id'], d['debit']))
            else:
                result = sorted(result, key = lambda d: (d['invoice_id']))
        return result
        
jasper_report.report_jasper('report.reconcile.ledger.jasper.report', 'reconcile.ledger.report', parser=jasper_ledger_report)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:-