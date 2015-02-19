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

class account_invoice_refund(osv.osv_memory):
    _inherit = 'account.invoice.refund'
    
    def compute_refund(self, cr, uid, ids, mode='refund', context=None):
        if context is None:
            context = {}
        res = super(account_invoice_refund, self).compute_refund(cr, uid, ids, mode=mode, context=context)
        if mode == 'refund' and res:
            invoice_pool = self.pool.get('account.invoice')
            invoice_id = context.get('active_id', False) or context.get('active_ids', False) and \
                                    context['active_ids'][0] or False
            domain = res.get('domain', False)
            if invoice_id and domain:
                id_domain_list = [x for x in domain if x[0] == 'id']
                refund_invoice_id = id_domain_list and id_domain_list[0] and id_domain_list[0][2] or False
                if refund_invoice_id:
                    invoice_pool.write(cr, uid, refund_invoice_id, {'refund_invoice_id': invoice_id},
                                       context=context)
        return res
    
account_invoice_refund()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
