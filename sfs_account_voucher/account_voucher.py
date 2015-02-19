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

from osv import fields,osv

class account_voucher_line(osv.osv):
    _inherit = "account.voucher.line"
    _columns = {
        'voucher_id': fields.many2one('account.voucher', 'Voucher', required=0, ondelete='cascade'),
                }
account_voucher_line()

class account_voucher(osv.osv):
    _inherit = 'account.voucher'
    _columns = {
                'partner_salesman_id': fields.related('partner_id', 'user_id', type='many2one', relation='res.users',
                                          store=True, string='Salesperson')
                }
account_voucher()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:-