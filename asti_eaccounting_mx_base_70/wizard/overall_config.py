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
import csv
import os.path
import tools
import base64
import StringIO

class overall_config_wizard(osv.osv_memory):
    _name = 'overall.config.wizard'
    _columns = {'action_status': fields.char('', size=128),
     'sat_filename': fields.char('Filename', size=128),
     'sat_data': fields.binary('Archivo de importaci\xc3\xb3n', filters='*.csv', help='Si ning\xc3\xban archivo es seleccionado se usar\xc3\xa1 el CSV instalado por defecto.'),
     'sat_catalog': fields.selection([('eaccount.bank', 'Bancos oficiales'),
                     ('account.journal.types', 'Tipos de poliza'),
                     ('sat.account.code', 'Codigo agrupador'),
                     ('eaccount.currency', 'Monedas'),
                     ('eaccount.payment.methods', 'Metodos de pago')], string='Catalogo objetivo'),
     'init_period_id': fields.many2one('account.period', 'Periodo de inicializacion')}
    _defaults = {'sat_catalog': lambda *a: 'sat.account.code'}
    _period_names = {'01': 'Enero',
     '02': 'Febrero',
     '03': 'Marzo',
     '04': 'Abril',
     '05': 'Mayo',
     '06': 'Junio',
     '07': 'Julio',
     '08': 'Agosto',
     '09': 'Septiembre',
     '10': 'Octubre',
     '11': 'Noviembre',
     '12': 'Diciembre'}
    _MODULE_DIRECTORY = 'asti_eaccounting_mx_base_70/loadable_data/'

    def fields_view_get(self, cr, uid, view_id = None, view_type = 'form', context = None, toolbar = False, submenu = False):
        if context is None:
            context = {}
        if context.get('launched_from_menu', False):
            val = super(overall_config_wizard, self).fields_view_get(cr, uid, view_id, view_type, context, toolbar, submenu)
            user = self.pool.get('res.users').browse(cr, uid, uid)
            return user.company_id._check_validity(val)
        return super(overall_config_wizard, self).fields_view_get(cr, uid, view_id, view_type, context, toolbar, submenu)

    def process_catalogs(self, cr, uid, ids, context):
        form = self.browse(cr, uid, ids)[0]
        user = self.pool.get('res.users').browse(cr, uid, uid)
        expected_col_number = 3 if form.sat_catalog == 'eaccount.bank' else 2
        orm_obj = self.pool.get(form.sat_catalog)
        if form.sat_data:
            decoded_string = base64.decodestring(form.sat_data)
            iterable_data = StringIO.StringIO(decoded_string)
        else:
            addons_paths = tools.config['addons_path'].split(',')
            if len(addons_paths) == 1:
                target_file = os.path.join(addons_paths[0], self._MODULE_DIRECTORY)
            else:
                for pth in addons_paths:
                    for subdir in sorted(os.listdir(pth)):
                        if subdir in self._MODULE_DIRECTORY:
                            target_file = os.path.join(pth, self._MODULE_DIRECTORY)
                            break

            if form.sat_catalog == 'eaccount.bank':
                target_file += 'banks'
            elif form.sat_catalog == 'account.journal.types':
                target_file += 'journal_types'
            elif form.sat_catalog == 'sat.account.code':
                target_file += 'sat_codes'
            elif form.sat_catalog == 'eaccount.payment.methods':
                target_file += 'payment_methods'
            else:
                target_file += 'currencies'
            target_file += '.csv'
            iterable_data = open(target_file, 'r').readlines()
        reader = csv.reader(iterable_data)
        if context is None:
            context = {}
        context['allow_management'] = True
        obj_fields = []
        vals = {}
        if form.sat_catalog == 'eaccount.bank':
            search_field = 'bic'
        elif form.sat_catalog == 'sat.account.code':
            search_field = 'key'
        else:
            search_field = 'code'
        for (idx, row,) in enumerate(reader):
            if len(row) < expected_col_number:
                self.write(cr, uid, ids, {'action_status': 'Formato inesperado. Se esperaban %s columnas, pero se encontraron %s. Linea %s' % (expected_col_number, len(row), idx + 1)})
                return True
            if idx == 0:
                obj_fields = row
                continue
            for (pos, fld,) in enumerate(obj_fields):
                vals[fld] = row[pos].zfill(3) if fld == search_field and form.sat_catalog in ('eaccount.bank', 'eaccount.currency') else row[pos]

            if form.sat_catalog == 'eaccount.currency':
                vals['company_id'] = user.company_id.id
            stored_ids = orm_obj.search(cr, uid, [(search_field, '=', vals[search_field])])
            if len(stored_ids):
                orm_obj.write(cr, uid, stored_ids, vals, context)
            else:
                orm_obj.create(cr, uid, vals, context)

        if form.sat_catalog == 'eaccount.bank':
            status = 'Los Bancos han sido correctamente procesados.'
        elif form.sat_catalog == 'account.journal.types':
            status = 'Los Tipos de Poliza han sido correctamente procesados.'
        elif form.sat_catalog == 'sat.account.code':
            status = 'Los Codigos del SAT han sido correctamente procesados.'
        elif form.sat_catalog == 'eaccount.payment.methods':
            status = 'Los metodos de pago han sido correctamente procesados.'
        else:
            status = 'Las monedas han sido correctamente procesadas.'
        self.write(cr, uid, ids, {'action_status': status})
        return {'type': 'ir.actions.act_window',
         'view_mode': 'form',
         'view_type': 'form',
         'res_id': ids[0],
         'res_model': self._name,
         'target': 'new',
         'name': 'Asistente para configuracion general - Contabilidad Electronica'}

    def process_accounts(self, cr, uid, ids, context):
        user = self.pool.get('res.users').browse(cr, uid, uid)
        if user.company_id.accounts_config_done:
            self.write(cr, uid, ids, {'action_status': 'Las cuentas en su catalogo ya habian sido inicializadas. Ningun cambio realizado.'})
            return {'type': 'ir.actions.act_window',
             'view_mode': 'form',
             'view_type': 'form',
             'res_id': ids[0],
             'res_model': self._name,
             'target': 'new',
             'name': 'Asistente para configuracion general'}
        form = self.browse(cr, uid, ids)[0]
        accountObj = self.pool.get('account.account')
        periodsObj = self.pool.get('account.period')
        accountIds = accountObj.search(cr, uid, [('company_id', '=', user.company_id.id)])
        accounts = accountObj.browse(cr, uid, accountIds)
        for acc in accounts:
            cr.execute("SELECT date_trunc('day', create_date) FROM account_account WHERE id = %s", (acc.id,))
            create_date = cr.fetchall()[0][0]
            if not create_date:
                raise osv.except_osv(u'Inconsistencia de informacion', u'La cuenta %s no tiene una fecha de creacion asignada' % acc.name_get())
            create_period_ids = [form.init_period_id.id] if form.init_period_id else periodsObj.search(cr, uid, [('date_start', '=', create_date[0:8] + '01')])
            if not len(create_period_ids):
                raise osv.except_osv(u'Informacion faltante', 'Se necesita crear el periodo fiscal %s / %s' % (self._period_names[create_date[5:7]], create_date[0:4]))
            accountObj.write(cr, uid, [acc.id], {'first_period_id': create_period_ids[0]})

        user.company_id.write({'accounts_config_done': True})
        self.write(cr, uid, ids, {'action_status': 'Todas las cuentas han sido procesadas exitosamente'})
        return {'type': 'ir.actions.act_window',
         'view_mode': 'form',
         'view_type': 'form',
         'res_id': ids[0],
         'res_model': self._name,
         'target': 'new',
         'name': 'Asistente para configuracion general - Contabilidad Electronica'}

overall_config_wizard()
