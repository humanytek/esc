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

from openerp.osv import osv, fields

import time

class reconcile_ledger_report(osv.TransientModel):
    _name = 'reconcile.ledger.report'
    _description = 'Model to print partner ledger report'
    
    def _get_fiscalyear(self, cr, uid, context=None):
        if context is None:
            context = {}
        now = time.strftime('%Y-%m-%d')
        company_id = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.id
        domain = [('company_id', '=', company_id), ('date_start', '<', now), ('date_stop', '>', now)]
        fiscalyears = self.pool.get('account.fiscalyear').search(cr, uid, domain, limit=1)
        return fiscalyears and fiscalyears[0] or False
    
    def _get_all_journal(self, cr, uid, context=None):
        return self.pool.get('account.journal').search(cr, uid ,[])
    
    def onchange_filter(self, cr, uid, ids, filter='none', fiscalyear_id=False, context=None):
        res = {'value': {}}
        if filter == 'none':
            res['value'] = {'period_from_id': False, 'period_to_id': False, 'date_from': False ,'date_to': False}
        if filter == 'date':
            res['value'] = {'period_from_id': False, 'period_to_id': False, 'date_from': time.strftime('%Y-01-01'), 'date_to': time.strftime('%Y-%m-%d')}
        if filter == 'period' and fiscalyear_id:
            start_period = end_period = False
            cr.execute('''
                SELECT * FROM (SELECT p.id
                               FROM account_period p
                               LEFT JOIN account_fiscalyear f ON (p.fiscalyear_id = f.id)
                               WHERE f.id = %s
                               AND p.special = false
                               ORDER BY p.date_start ASC, p.special ASC
                               LIMIT 1) AS period_start
                UNION ALL
                SELECT * FROM (SELECT p.id
                               FROM account_period p
                               LEFT JOIN account_fiscalyear f ON (p.fiscalyear_id = f.id)
                               WHERE f.id = %s
                               AND p.date_start < NOW()
                               AND p.special = false
                               ORDER BY p.date_stop DESC
                               LIMIT 1) AS period_stop''', (fiscalyear_id, fiscalyear_id))
            periods =  [i[0] for i in cr.fetchall()]
            if periods and len(periods) > 1:
                start_period = periods[0]
                end_period = periods[1]
            res['value'] = {'period_from_id': start_period, 'period_to_id': end_period, 'date_from': False, 'date_to': False}
        return res
    
    _columns = {
                'fiscalyear_id': fields.many2one('account.fiscalyear', 'Fiscal Year'),
                'way': fields.selection([('debit_to_credit', 'Customer Payments'),
                                         ('credit_to_debit', 'Supplier Payments')], 'Way'),
                'filter': fields.selection([('none', 'None'), ('date', 'Date'), ('period', 'Period')],
                                           'Filter By'),
                'date_from': fields.date('Date From'),
                'date_to': fields.date('Date To'),
                'period_from_id': fields.many2one('account.period', 'Period From'),
                'period_to_id': fields.many2one('account.period', 'Period To'),
                'journal_ids': fields.many2many('account.journal', 'journal_wizard_rel', 'wizard_id', 'journal_id',
                                                'Journal')
                }

    _defaults = {
                 'fiscalyear_id': _get_fiscalyear,
                 'journal_ids': _get_all_journal,
                 'way': 'debit_to_credit',
                 'filter': 'none',
                 'way': 'debit_to_credit'
                 }
    
    def print_report(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        data = self.read(cr, uid, ids, [], context=context)[0]
        return {
                'type': 'ir.actions.report.xml',
                'report_name': 'reconcile.ledger.jasper.report',
                'datas': data,
                'context': context
                }
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:-