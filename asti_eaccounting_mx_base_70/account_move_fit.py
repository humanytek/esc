# -*- coding: utf-8 -*-
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
import re
_RFC_PATTERN = re.compile('[A-ZÑ&]{3,4}[0-9]{2}[0-1][0-9][0-3][0-9][A-Z0-9]?[A-Z0-9]?[0-9A-Z]?')
_SERIES_PATTERN = re.compile('[A-Z]+')
_UUID_PATTERN = re.compile('[a-f0-9A-F]{8}-[a-f0-9A-F]{4}-[a-f0-9A-F]{4}-[a-f0-9A-F]{4}-[a-f0-9A-F]{12}')

class account_move_fit(osv.osv):
    _inherit = 'account.move'
    _columns = {'item_concept': fields.char('Concepto', size=300),
     'complement_line_ids': fields.one2many('eaccount.complements', 'move_id')}
    _PERIOD_NAMES = {'01': 'ENERO',
     '02': 'FEBRERO',
     '03': 'MARZO',
     '04': 'ABRIL',
     '05': 'MAYO',
     '06': 'JUNIO',
     '07': 'JULIO',
     '08': 'AGOSTO',
     '09': 'SEPTIEMBRE',
     '10': 'OCTUBRE',
     '11': 'NOVIEMBRE',
     '12': 'DICIEMBRE'}

    def launch_period_validator(self, cr, uid, ids, context):
        if self.pool.get('res.users').browse(cr, uid, uid).company_id._check_validity():
            raise osv.except_osv(u'Licenciamiento de contabilidad electronica no valido', u'Ha cambiado sus datos de empresa recientemente?')
        if not len(context['active_ids']):
            raise osv.except_osv(u'Ningun registro seleccionado', u'Debe seleccionar al menos una poliza para procesar.')
        moves = self.browse(cr, uid, context['active_ids'])
        all_periods = set([ x.period_id for x in moves ])
        if len(all_periods) > 1:
            raise osv.except_osv(u'Se ha encontrado mes de un periodo fiscal', u'Todas las polizas seleccionadas deben pertenecer al mismo periodo fiscal.')
        period_id = all_periods.pop()
        context['period_id'] = period_id.id
        return {'type': 'ir.actions.act_window',
         'res_model': 'vouchers.xml.creator',
         'view_mode': 'form',
         'view_type': 'form',
         'name': 'Parametros del XML',
         'target': 'new',
         'context': context}

    def post(self, cr, uid, ids, context = None):
        for mid in ids:
            move = self.browse(cr, uid, mid)
            for ln in move.line_id:
                if not len([ x for x in ln.complement_line_ids if x.type_key == 'cfdi' ]) and ln.account_id.apply_in_cfdi:
                    raise osv.except_osv(u'Complemento faltante', u'La cuenta "%s" este configurada para asignar al menos un CFDI en sus asientos.' % ln.account_id.name)
                if not len([ x for x in ln.complement_line_ids if x.type_key == 'other' ]) and ln.account_id.apply_in_other:
                    raise osv.except_osv(u'Complemento faltante', u'La cuenta "%s" este configurada para asignar al menos un CFD / CBB en sus asientos.' % ln.account_id.name)
                if not len([ x for x in ln.complement_line_ids if x.type_key == 'foreign' ]) and ln.account_id.apply_in_forgn:
                    raise osv.except_osv(u'Complemento faltante', u'La cuenta "%s" este configurada para asignar al menos un comprobante extranjero en sus asientos.' % ln.account_id.name)
                if not len([ x for x in ln.complement_line_ids if x.type_key == 'check' ]) and ln.account_id.apply_in_check:
                    raise osv.except_osv(u'Complemento faltante', u'La cuenta "%s" este configurada para asignar al menos un cheque en sus asientos.' % ln.account_id.name)
                if not len([ x for x in ln.complement_line_ids if x.type_key == 'transfer' ]) and ln.account_id.apply_in_trans:
                    raise osv.except_osv(u'Complemento faltante', u'La cuenta "%s" este configurada para asignar al menos una transferencia en sus asientos.' % ln.account_id.name)
                if not len([ x for x in ln.complement_line_ids if x.type_key == 'payment' ]) and ln.account_id.apply_in_paymth:
                    raise osv.except_osv(u'Complemento faltante', u'La cuenta "%s" este configurada para asignar al menos un metodo de pago en sus asientos.' % ln.account_id.name)
                for cmpl in ln.complement_line_ids + move.complement_line_ids:
                    location = ' en Auxiliar de folios' if cmpl.move_id else ' en complementos por asiento'
                    if cmpl.origin_bank_id and not cmpl.origin_bank_id.sat_bank_id:
                        raise osv.except_osv('Datos faltantes' + location, u'El banco "%s" no tiene asignado un codigo del SAT' % cmpl.origin_bank_id.name)
                    if cmpl.origin_bank_id and cmpl.origin_bank_id.sat_bank_id.bic == '999' and not cmpl.origin_frgn_bank:
                        raise osv.except_osv('Datos faltantes' + location, u'El banco "%s" este marcado como extranjero, pero una linea de su complemento no contiene el nombre del banco.' % cmpl.origin_bank_id.name)
                    if cmpl.destiny_bank_id and not cmpl.destiny_bank_id.sat_bank_id:
                        raise osv.except_osv('Datos faltantes' + location, u'El banco "%s" no tiene asignado un codigo del SAT' % cmpl.destiny_bank_id.name)
                    if cmpl.destiny_bank_id and cmpl.destiny_bank_id.sat_bank_id.bic == '999' and not cmpl.destiny_frgn_bank:
                        raise osv.except_osv('Datos faltantes' + location, u'El banco "%s" este marcado como extranjero, pero una linea de su complemento no contiene el nombre del banco.' % cmpl.destiny_bank_id.name)
                    if cmpl.uuid and len(cmpl.uuid) != 36 or cmpl.uuid and not _UUID_PATTERN.match(cmpl.uuid.upper()):
                        raise osv.except_osv(u'Informacion incorrecta' + location, u'El UUID "%s" no se apega a los lineamientos del SAT.' % cmpl.uuid)
                    if cmpl.rfc and not _RFC_PATTERN.match(cmpl.rfc):
                        raise osv.except_osv(u'Informacion incorrecta' + location, u'El RFC "%s" no es valido con respecto a los lineamientos del SAT.' % cmpl.rfc)
                    if cmpl.rfc2 and not _RFC_PATTERN.match(cmpl.rfc2):
                        raise osv.except_osv(u'Informacion incorrecta' + location, u'El RFC "%s" no es valido con respecto a los lineamientos del SAT.' % cmpl.rfc2)
                    if cmpl.cbb_series and not _SERIES_PATTERN.match(cmpl.cbb_series):
                        raise osv.except_osv(u'Informacion incorrecta' + location, u'La "Serie" en el comprobante solo debe contener letras.')

        return super(account_move_fit, self).post(cr, uid, ids, context)

    def edit_complements(self, cr, uid, ids, context = None):
        view_id = self.pool.get('ir.ui.view').search(cr, uid, [('name', 'ilike', 'move.complements.form')])
        return {'type': 'ir.actions.act_window',
         'res_id': ids[0],
         'res_model': 'account.move',
         'view_mode': 'form',
         'view_type': 'form',
         'target': 'new',
         'view_id': view_id[0],
         'name': u'Contabilidad electronica - auxiliares de folios'}

    def save_complements(self, cr, uid, ids, context = None):
        return True

account_move_fit()

class vouchers_xml_holder(osv.osv_memory):
    _name = 'vouchers.xml.creator'
    _columns = {'vouchers_reqtype': fields.selection([('AF', 'Acto de fiscalizacion'),
                          ('FC', 'Fiscalizacion compulsa'),
                          ('DE', 'Devolucion'),
                          ('CO', 'Compensacion')], string='Tipo de solicitud', required=True),
     'vouchers_ordnum': fields.char('Numero de orden', size=13),
     'vouchers_procnum': fields.char('Numero de tramite', size=10)}
    _defaults = {'vouchers_reqtype': lambda *a: 'DE'}

    def start_processing(self, cr, uid, ids, context):
        form = self.browse(cr, uid, ids)[0]
        period = self.pool.get('account.period').browse(cr, uid, context['period_id'])
        wizVals = {'xml_target': context.get('target', 'vouchers'),
         'month': period.date_start[5:7],
         'year': int(period.date_start[0:4]),
         'request_type': form.vouchers_reqtype,
         'order_number': form.vouchers_ordnum,
         'procedure_number': form.vouchers_procnum}
        wizardObj = self.pool.get('files.generator.wizard')
        wizId = wizardObj.create(cr, uid, wizVals)
        return wizardObj.process_file(cr, uid, [wizId], context, moveIds=context['active_ids'])

vouchers_xml_holder()
