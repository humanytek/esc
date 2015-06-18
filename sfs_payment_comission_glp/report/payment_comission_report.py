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

import tools
import openerp.addons.decimal_precision as dp

class payment_comission_report(osv.osv):
    _name = 'payment.comission.report'
    _description = 'Analysis report to view comission for user'
    _auto = False
    _rec_name = 'partner_id'
    _columns = {
                'partner_id': fields.many2one('res.partner', 'Customer Name'),
                'payment_term_id': fields.many2one('account.payment.term', 'Invoice Payment Term'),
                'journal_id': fields.many2one('account.journal', 'Account Journal'),
                'due_date': fields.date('Due Date'),
                'invoice_amount': fields.float('Invoice Amount', digits_compute=dp.get_precision('Account')),
                'payment_date': fields.date('Payment Date'),
                'payment_amount': fields.float('Payment Amount', digits_compute=dp.get_precision('Account')),
                'user_id': fields.many2one('res.users', 'Salesperson'),
                'due_days': fields.integer('Days Due'),
                'comission_percent': fields.float('Percent Commission'),
                'penalization_amount': fields.float('Amount Penalization', digits_compute=dp.get_precision('Account')),
                'penalization_percent': fields.char('Penalization Percent', size=64),
                'comission': fields.float('Commission', digits_compute=dp.get_precision('Account')),
                'account_move_line_id': fields.many2one('account.move.line', 'Journal Item')
                }
    
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'payment_comission_report')
        cr.execute("""CREATE OR REPLACE FUNCTION get_history_ids
                   ()
                   RETURNS TABLE(ids integer) AS
                   $BODY$
                   BEGIN
                   return query
           SELECT DISTINCT ON (uth.invoice_id) uth.id FROM user_transaction_history uth 
           LEFT JOIN account_invoice ai on ai.id = uth.invoice_id
           WHERE uth.transaction_type='payment' and ai.state = 'paid'
           ORDER BY uth.invoice_id, uth.transaction_date desc;
                   END
                   $BODY$
                   LANGUAGE 'plpgsql';
           CREATE OR REPLACE FUNCTION get_penalization_percent
                   (due_days integer)
                   RETURNS TABLE(penalization_percent float) AS
                   $BODY$
                   BEGIN
                   return query
           SELECT penelization_percent FROM penalization_rule_line prl
           LEFT JOIN penalization_rule pr ON pr.id = prl.penalization_id
           WHERE pr.active = true AND
           prl.qty <= due_days
           ORDER BY prl.qty desc
           limit 1;
                   END
                   $BODY$
                   LANGUAGE 'plpgsql';
           create or replace view payment_comission_report as (SELECT
                x.id AS id,
                x.partner_id AS partner_id,
                x.payment_term_id AS payment_term_id,
                x.journal_id AS journal_id,
                x.due_date AS due_date,
                x.invoice_amount AS invoice_amount,
                x.payment_date AS payment_date,
                x.payment_amount AS payment_amount,
                x.user_id AS user_id,
                x.account_move_line_id as account_move_line_id,
                case 
                    when x.due_days < 0.00 then 0.00 else x.due_days end AS due_days,
                x.comission_percent AS comission_percent,
                ((x.invoice_amount - x.refund_amount) * (x.comission_percent/100)) * (x.penalization_percent/100) AS penalization_amount,
                x.penalization_percent || '%' AS penalization_percent,
                (((x.invoice_amount - x.refund_amount) * (x.comission_percent/100))) - (((x.invoice_amount - x.refund_amount) * (x.comission_percent/100)) * (x.penalization_percent/100)) AS comission
           FROM
                (SELECT ai.id AS id,
                    ai.partner_id AS partner_id,
                    apt.id AS payment_term_id,
                    ai.journal_id AS journal_id,
                    ai.date_due AS due_date,
                    COALESCE(ai.amount_untaxed, 0.00) AS invoice_amount,
                    uth.transaction_date AS payment_date,
                    uth.amount AS payment_amount,
                    rp.user_id AS user_id,
                    uth.move_line_id as account_move_line_id,
                    uth.transaction_date - ai.date_due AS due_days,
                    COALESCE(rp.comission_percent, 0.00) AS comission_percent,
                    COALESCE((SELECT get_penalization_percent(uth.transaction_date - ai.date_due)), 0.00) AS penalization_percent,
                    COALESCE((SELECT 
                        sum(uth1.amount)
                     FROM 
                        user_transaction_history uth1
                     WHERE 
                        uth1.invoice_id = uth.invoice_id AND uth1.transaction_type = 'refund'), 0.00) AS refund_amount
                FROM 
                    user_transaction_history uth
                LEFT JOIN account_invoice ai ON ai.id = uth.invoice_id
                LEFT JOIN account_payment_term apt ON apt.id = ai.payment_term
                LEFT JOIN res_partner rp ON rp.id = ai.partner_id
                WHERE uth.id IN (SELECT get_history_ids())
                ORDER BY ai.id)x)
        """)

payment_comission_report()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
