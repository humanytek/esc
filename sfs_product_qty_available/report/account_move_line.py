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

import tools
from osv import  osv
import openerp.addons.decimal_precision as dp

class account_move_line_report(osv.osv):
    _name = 'account.move.line.report'
    _auto = False
    
    def init(self, cr):
        tools.drop_view_if_exists(cr, 'account_move_line_report')
        cr.execute(""" 
                   create or replace view account_move_line_report as (
                       select
                           aml.id as id,
                           aml.name as name,
                           aml.date as date,
                           aml.account_id as account_id,
                           aml.currency_id as currency_id,
                           aml.debit as debit,
                           aml.credit as credit,
                           aml.ref as ref,
                           aml.journal_id as journal_id,
                           aml.period_id as period_id,
                           aml.reconcile_id as reconcile_id,
                           aml.move_id as move_id,
                           aml.tot_balance as tot_balance,
                           res.id as partner_id
                           
                           
                       from account_move_line as aml
                            left join res_partner res on (aml.partner_id=res.id)
                       group by
                            aml.id,
                            res.id
                            
                        )
                   """)

account_move_line_report()  
    
    
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: