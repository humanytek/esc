##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2010-2015 Humanytek SAPI de CV (<http://www.humanytek.com>). 
#    All Rights Reserved
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

from osv import fields, osv

class moveline_info_manager(osv.osv_memory):
    _name = 'moveline.info.manager'
    _columns = {'line_id': fields.many2one('account.move.line', 'Line id', required=True),
     'line_name': fields.related('line_id', 'name', type='char', string='Nombre', readonly=True),
     'line_account': fields.related('line_id', 'account_id', type='many2one', relation='account.account', string='Cuenta', readonly=True),
     'debit': fields.related('line_id', 'debit', type='float', string='Debe', readonly=True),
     'credit': fields.related('line_id', 'credit', type='float', string='Haber', readonly=True),
     'check_ids': fields.related('line_id', 'check_ids', type='one2many', relation='move.line.checks', string='Cheques'),
     'transfer_ids': fields.related('line_id', 'transfer_ids', type='one2many', relation='move.line.transfers', string='Transferencias'),
     'cfdi_ids': fields.related('line_id', 'cfdi_ids', type='one2many', relation='move.line.cfdis', string='CFDI')}

    def save_changes(self, cr, uid, ids, context):
        return {'type': 'ir.actions.act_window_close'}

moveline_info_manager()
