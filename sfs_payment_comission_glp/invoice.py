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

class account_invoice(osv.Model):
    _inherit = 'account.invoice'
    _columns = {
                'refund_invoice_id': fields.many2one('account.invoice', 'Related Invoice')
                }
    
    def onchange_partner_id(self,  cr, uid, ids, type, partner_id,\
            date_invoice=False, payment_term=False, partner_bank_id=False, company_id=False):
        
        res = super(account_invoice, self).onchange_partner_id(cr, uid, ids, type, partner_id,\
            date_invoice, payment_term, partner_bank_id, company_id)
        if type == "out_refund" and partner_id:
            res_obj = self.pool.get('res.partner').browse(cr, uid, partner_id)
            res['value'].update({'user_id': res_obj.user_id and res_obj.user_id.id or False})
        return res
    
account_invoice()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
