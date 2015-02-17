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
from operator import itemgetter
from hmtk_crm_claim_customization import JasperDataParser
from jasper_reports import jasper_report

import pooler
from osv import fields, osv
import time
from datetime import datetime

class crm_claim_report(JasperDataParser.JasperDataParser):
    def __init__(self, cr, uid, ids, data, context):
        super(crm_claim_report, self).__init__(cr, uid, ids, data, context)

    def generate_data_source(self, cr, uid, ids, data, context):
        return 'xml_records'

    def generate_parameters(self, cr, uid, ids, data, context):
        return {'IS_IGNORE_PAGINATION':True}
    
    def generate_properties(self, cr, uid, ids, data, context):
        return {
            'net.sf.jasperreports.export.xls.one.page.per.sheet':'true',
            'net.sf.jasperreports.export.ignore.page.margins':'true',
            'net.sf.jasperreports.export.xls.remove.empty.space.between.rows':'true',
            'net.sf.jasperreports.export.xls.detect.cell.type': 'true',
            'net.sf.jasperreports.export.xls.white.page.background': 'true',
            'net.sf.jasperreports.export.xls.show.gridlines': 'true',
            }
    
   
    def generate_records(self, cr, uid, ids, data, context):
        result = []
        claim_obj = self.pool.get('crm.claim')
        user_pool = self.pool.get('res.users')
#         if context['lang'] != 'en_US':
#             data.update({'report_name': 'crm_claim_report_spanish'})
        
        for claim in claim_obj.browse(cr, uid, ids, context=context):
            user_name = ''
            if claim.partner_id:
                user_id = user_pool.search(cr, uid, [('partner_id', '=', claim.partner_id.id)], context=context)
                if user_id:
                    user_name = user_pool.browse(cr, uid, user_id[0], context=context).name
            data = {
                'name': claim.name or '',
                'claim_no': claim.claim_no or '',
                'date': claim.date and datetime.strptime(claim.date, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y') or '',
                'responsible':  claim.user_id and claim.user_id.name or '',
                'priority': claim.priority or '',
                'sales_team': claim.section_id.name or '',
                'deadline': claim.date_deadline and datetime.strptime(claim.date_deadline, '%Y-%m-%d').strftime('%d-%m-%Y') or '',
                'batch_type': claim.batch_type or '',
                'invoice_reference': claim.invoice_reference or '',
                'status': claim.state and claim.state.title() or '',
                'partner': claim.partner_id and claim.partner_id.name or '',
                'partner_phone': claim.partner_phone or '',
                'email_from': claim.email_from or '',
                'user_fault': claim.user_fault or '',
                'categ': claim.categ_id and claim.categ_id.name or '',
#                 'reference': claim.ref and claim.ref.title() or '',
                'm2o':claim.ref and claim.ref.name or '',
                'description': claim.description or '',
                'date_action_next': claim.date_action_next and datetime.strptime(claim.date_action_next, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y') or '',
                'action_next': claim.action_next or '',
                'create_date': claim.create_date and datetime.strptime(claim.create_date, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y') or '',
                'cause': claim.cause or '',
                'resolution': claim.resolution or '',
                'type_action': claim.type_action and claim.type_action.title() or '',
                'write_date': claim.write_date and datetime.strptime(claim.write_date, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y') or '',
                'date_closed': claim.date_closed and datetime.strptime(claim.date_closed, '%Y-%m-%d %H:%M:%S').strftime('%d-%m-%Y') or '',
                'user': user_name,
                
                
                }
            result.append(data)
        result = sorted(result, key=itemgetter('name'))
        return result

jasper_report.report_jasper('report.crm_claim_report', 'crm.claim', parser=crm_claim_report)
jasper_report.report_jasper('report.crm_claim_report_spanish', 'crm.claim', parser=crm_claim_report)
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: