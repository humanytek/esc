# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-2014 ZestyBeanz Technologies Pvt Ltd(<http://www.zbeanztech.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import fields, osv
from openerp.addons.base_status.base_stage import base_stage
class crm_claim(base_stage, osv.osv):
    def create(self, cr, uid, vals, context=None):
        if not vals.get('claim_no', False):
            vals['claim_no'] = self.pool.get('ir.sequence').get(cr, uid, 'crm.claim')
        return super(crm_claim, self).create(cr, uid, vals, context=context)
    _inherit = 'crm.claim'
    _rec_name = 'claim_no'
    _columns = {
        'batch_type': fields.char('Batch Type', size=64),
        'invoice_reference': fields.char('Invoice Reference', size=64),
        'claim_no': fields.char('Claim', size=128),
        'corrective_actions_permanent': fields.text('Corrective Actions Permanent'),
        'results_taken_consequences': fields.text('Results Taken Consequences'),
        'source': fields.selection([('reception', 'Reception'), ('customer_notification', 'Customer Notification'), ('auditing', 'Auditing')], 'Source'),
        }
    def print_claim(self, cr, uid, ids, context=None):
        data = self.read(cr, uid, ids[0], context=context)
        datas = {
             'ids': ids,
             'model': 'crm.claim',
             'form': data
        }
    
        if context['lang'] == 'en_US':
            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'crm_claim_report',
                'datas': datas,
                'nodestroy' : True,
                'name': 'Claim Report'
            }
        else:
            return {
                'type': 'ir.actions.report.xml',
                'report_name': 'crm_claim_report_spanish',
                'datas': datas,
                'nodestroy' : True,
                'name': 'Claim Report'
            }
crm_claim()
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
