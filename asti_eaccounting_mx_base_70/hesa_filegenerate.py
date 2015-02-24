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
from lxml import etree as et
import base64

class hesa_trialbalance_inherit(osv.osv):
    _inherit = 'account.monthly_balance'

    def launch_xml_generator(self, cr, uid, ids, context):
        if self.pool.get('res.users').browse(cr, uid, uid).company_id._check_validity():
            raise osv.except_osv(u'Licenciamiento de contabilidad electronica no valido', u'Ha cambiado sus datos de empresa recientemente?')
        if not len(context['active_ids']):
            raise osv.except_osv(u'Archivo vacio', 'No se ha seleccionado ninguna partida en la balanza.')
        return {'type': 'ir.actions.act_window',
         'res_model': 'hesa.filegenerate',
         'view_mode': 'form',
         'view_type': 'form',
         'name': 'Parametros para la balanza',
         'target': 'new',
         'context': context}

hesa_trialbalance_inherit()

class hesa_filegenerate(osv.osv_memory):
    _name = 'hesa.filegenerate'
    _columns = {'trial_delivery': fields.selection([('N', 'Normal'), ('C', 'Complementario')], string='Tipo de envio', required=True),
     'trial_lastchange_date': fields.date('Ultima modificacion contable')}
    _defaults = {'trial_delivery': 'N'}

    def generate_file(self, cr, uid, ids, context):
        form = self.browse(cr, uid, ids)[0]
        period_id = self.pool.get('account.monthly_balance').browse(cr, uid, context['active_ids'][0]).period_id
        chart = self.pool.get('account.account').search(cr, uid, [('parent_id', '=', False)])[0]
        wizard_vals = {'xml_target': 'trial_balance',
         'month': period_id.date_start[5:7],
         'year': int(period_id.date_start[0:4]),
         'trial_delivery': form.trial_delivery,
         'trial_lastchange_date': form.trial_lastchange_date,
         'accounts_chart': chart}
        wizardObj = self.pool.get('files.generator.wizard')
        wizId = wizardObj.create(cr, uid, wizard_vals)
        return wizardObj.process_file(cr, uid, [wizId], context, balance_ids=context['active_ids'])

hesa_filegenerate()
