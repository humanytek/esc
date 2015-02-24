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

from base64 import b64decode as b64dec, b64encode as b64enc
from osv import fields, osv
from lxml import etree as et
from M2Crypto import RSA, X509
from M2Crypto.EVP import MessageDigest
from StringIO import StringIO
from zipfile import ZipFile
import time
import os
import tools
import zipfile
import tempfile
import re
_RFC_PATTERN = re.compile('[A-ZÑ&]{3,4}[0-9]{2}[0-1][0-9][0-3][0-9][A-Z0-9]?[A-Z0-9]?[0-9A-Z]?')
_SERIES_PATTERN = re.compile('[A-Z]+')
_UUID_PATTERN = re.compile('[a-f0-9A-F]{8}-[a-f0-9A-F]{4}-[a-f0-9A-F]{4}-[a-f0-9A-F]{4}-[a-f0-9A-F]{12}')

class files_generator_wizard(osv.osv_memory):
    _name = 'files.generator.wizard'
    _columns = {'filename': fields.char('Filename', size=128),
     'primary_file': fields.binary('Primary file'),
     'stamped_file': fields.binary('Stamped file'),
     'zipped_file': fields.binary('Zipped file'),
     'xml_target': fields.selection([('accounts_catalog', 'Catalogo de cuentas'),
                    ('trial_balance', 'Balanza de comprobacion'),
                    ('vouchers', 'Informacion de polizas'),
                    ('helpers', 'Auxiliar de folios')], string='XML a generar'),
     'state': fields.selection([('init', 'Init'),
               ('val_xcpt', 'Val Except'),
               ('val_done', 'Val Done'),
               ('stamp_xcpt', 'Stamp Except'),
               ('stamp_done', 'Stamp Done'),
               ('zip_done', 'Zip done')], string='State'),
     'month': fields.selection([('01', 'Enero'),
               ('02', 'Febrero'),
               ('03', 'Marzo'),
               ('04', 'Abril'),
               ('05', 'Mayo'),
               ('06', 'Junio'),
               ('07', 'Julio'),
               ('08', 'Agosto'),
               ('09', 'Septiembre'),
               ('10', 'Octubre'),
               ('11', 'Noviembre'),
               ('12', 'Diciembre'),
               ('13', '-- Cierre --')], 'Periodo', required=True),
     'trial_delivery': fields.selection([('N', 'Normal'), ('C', 'Complementaria')], string='Tipo de envio', required=True),
     'trial_lastchange_date': fields.date('Ultima modificacion contable'),
     'request_type': fields.selection([('AF', 'Acto de fiscalizacion'),
                      ('FC', 'Fiscalizacion compulsa'),
                      ('DE', 'Devolucion'),
                      ('CO', 'Compensacion')], string='Tipo de solicitud', attrs={'required': [('xml_target', '=', 'vouchers')]}),
     'order_number': fields.char('Numero de orden', size=13),
     'procedure_number': fields.char('Numero de tramite', size=10),
     'year': fields.integer('Ejercicio', required=True),
     'accounts_chart': fields.many2one('account.account', 'Plan contable', domain=[('parent_id', '=', False)])}
    _defaults = {'state': lambda *a: 'init',
     'xml_target': lambda *a: 'accounts_catalog',
     'year': lambda *a: int(time.strftime('%Y')),
     'trial_delivery': lambda *a: 'N',
     'request_type': lambda *a: 'DE'}
    _XSI_DECLARATION = 'http://www.w3.org/2001/XMLSchema-instance'
    _SAT_NS = {'xsi': _XSI_DECLARATION}
    _ACCOUNTS_CATALOG_URI = 'www.sat.gob.mx/esquemas/ContabilidadE/1_1/CatalogoCuentas'
    _TRIAL_BALANCE_URI = 'www.sat.gob.mx/esquemas/ContabilidadE/1_1/BalanzaComprobacion'
    _VOUCHERS_URI = 'www.sat.gob.mx/esquemas/ContabilidadE/1_1/PolizasPeriodo'
    _HELPERS_URI = 'www.sat.gob.mx/esquemas/ContabilidadE/1_1/AuxiliarFolios'

    def _outputXml(self, output):
        return et.tostring(output, pretty_print=True, xml_declaration=True, encoding='UTF-8')

    def _reopen_wizard(self, res_id):
        return {'type': 'ir.actions.act_window',
         'res_id': res_id,
         'view_mode': 'form',
         'view_type': 'form',
         'res_model': 'files.generator.wizard',
         'target': 'new',
         'name': 'Contabilidad electronica'}

    def _xml_from_dict(self, node, namespaces, nsuri, parent = None):
        """
         Recursively builds an XML tree from a two elements tuple passed in the 'content' parameter.
        Consider that this method is prepared only to generate nodes, attributes and content in the
        form of child nodes; moreover, all the elements will be qualified using the specified nsuri
        and prefix. 
         Each element of that list represents a node or set of nodes that will be created. Each tuple
        contains two positions: 
        Position 0: tag of a new element to be created or the key word 'unroot' to indicate that no
                    new element is needed.
        Position 1: value for the element. This can either be a list of tuples or any other object. When
                    a list is found, content for the element will be created from it using recursive
                    calls to this method. When any other type is found, an attribute for the element 
                    will be created; if a string value is passed then the attribute is appended as-is,
                    otherwise a new string is created from the value and then used to append a new
                    attribute.
              
        Consider the following lines of code
        
        data = [
                ('root', [('at', 'val'), ('at1', 12),
                          ('el', [('at0', True), 
                                  ('subel0', [('at0', 'val0'), ('at01', 34.987)]),
                                  ('subel1', [('at1', -123), ('unroot', [
                                                                         ('child', [('at', 'val')])
                                                                        ]
                                                            )
                                            ]
                                )
                                ]
                          ),
                          ('el1', [('subel11', [('at0', False)])
                                   ('subel12', [
                                                ('child', [('at', 'val')])
                                               ])]
                          )
                        ]
                 )
            ]
                
        Applying the rules outlined above, the resulting XML generated by this method is
        
        <?xml version="1.0" coding="UTF-8"?>
            <root at="val" at1="12">
                <el at0="True">
                    <subel0 at0="val0" at01="34.987"/>
                    <subel1 at1="-123">
                        <child at="val"/>
                    </subel1>
                </el>
                <el1>
                    <subel11 at0="False"/>
                    <subel12>
                        <child1 at1="val1"/>
                    </subel12>
                </el1>
            </root>
        
        """
        attrs = {}
        attrs.update({elm[0]:elm[1] if type(elm[1]) in (str, unicode) else str(elm[1]) for elm in node[1] if not isinstance(elm[1], list)})
        children = [ elm for elm in node[1] if isinstance(elm[1], list) ]
        currNode = et.Element('{' + nsuri + '}' + node[0], attrib=attrs, nsmap=namespaces) if node[0] != 'unroot' else parent
        for chl in children:
            child = self._xml_from_dict(chl, namespaces, nsuri, currNode)
            currNode.append(child)

        return currNode

    def _validate_xml(self, cr, uid, schema, xmlTree, filename):
        validationResult = 'val_done'
        schema_path = self._find_file_in_addons('asti_eaccounting_mx_base_70/sat_xsd', schema)
        try:
            schema_file = open(schema_path, 'r')
        except IOError:
            raise osv.except_osv('Esquema XSD no encontrado', u'El esquema de validacion de SAT no fue encontrado en la ruta "%s"' % schema_path[0:schema_path.find(schema)])
        schemaXml = et.parse(schema_file)
        try:
            schema = et.XMLSchema(schemaXml)
        except et.XMLSchemaParseError:
            if 'accounts_catalog' in schema_path:
                newLocation = schema_path.replace('accounts_catalog', 'complex_types')
            elif 'vouchers' in schema_path:
                newLocation = schema_path.replace('vouchers', 'complex_types')
            else:
                newLocation = schema_path.replace('helpers', 'complex_types')
            schemaXml.find('{http://www.w3.org/2001/XMLSchema}import').attrib['schemaLocation'] = newLocation
            try:
                schema = et.XMLSchema(schemaXml)
                validationResult = 'val_xcpt'
            except:
                schema = None
        if schema is None:
            raise osv.except_osv(u'Error al cargar esquema de validacion', 'Por favor realize nuevamente el procesamiento del archivo.')
        try:
            schema.assertValid(xmlTree)
            return validationResult
        except et.DocumentInvalid as ex:
            error_haul = u'Los siguientes errores fueron encontrados:\n\n'
            error_haul += u'\n'.join([ u'Linea: %s\nTipo: %s\nMensaje: %s\n**********' % (err.line, err.type_name, err.message) for err in ex.error_log ])
            xsdhandler_id = self.pool.get('xsdvalidation.handler.wizard').create(cr, uid, {'error_file': b64enc(error_haul.encode('UTF-8')),
             'error_filename': 'errores.txt',
             'sample_xml': b64enc(self._outputXml(xmlTree)),
             'sample_xmlname': filename})
            return {'type': 'ir.actions.act_window',
             'res_model': 'xsdvalidation.handler.wizard',
             'res_id': xsdhandler_id,
             'view_mode': 'form',
             'view_type': 'form',
             'target': 'new',
             'name': 'La validacion del archivo generado fallo.'}

    def _find_file_in_addons(self, directory, filename):
        """To use this method, specify a filename and the directory where it resides.
        Said directory must be at the first level for the modules folders."""
        addons_paths = tools.config['addons_path'].split(',')
        if len(addons_paths) == 1:
            return os.path.join(addons_paths[0], directory, filename)
        for pth in addons_paths:
            for subdir in os.listdir(pth):
                if subdir in directory:
                    return os.path.join(pth, directory, filename)

        return False

    def fields_view_get(self, cr, uid, view_id = None, view_type = 'form', context = None, toolbar = False, submenu = False):
        original_req = super(files_generator_wizard, self).fields_view_get(cr, uid, view_id, view_type, context, toolbar, submenu)
        if context is None:
            context = {}
        if context.get('launched_from_menu', False):
            user = self.pool.get('res.users').browse(cr, uid, uid)
            return user.company_id._check_validity(original_req)
        return original_req

    def process_file(self, cr, uid, ids, context, account_ids = None, balance_ids = None, moveIds = None):
        form = self.browse(cr, uid, ids)[0]
        user = self.pool.get('res.users').browse(cr, uid, uid)
        if len(user.company_id.rfc) < 12 or len(user.company_id.rfc) > 13 or not _RFC_PATTERN.match(user.company_id.rfc):
            raise osv.except_osv(u'Datos de compania erroneos', u'El RFC "%s" no es valido con respecto a los lineamientos del SAT.' % user.company_id.rfc)
        if form.year < 2015:
            raise osv.except_osv('Fecha fuera de rango', 'La contabilidad electronica comienza a reportarse a partir del 2015.')
        if not user.company_id.rfc:
            raise osv.except_osv(u'Informacion faltante', 'No se ha configurado un R.F.C. para la empresa')
        periodObj = self.pool.get('account.period')
        period_ids = periodObj.search(cr, uid, [('date_start', '=', str(form.year) + '-' + form.month + '-01')])
        if not len(period_ids):
            raise osv.except_osv(u'Informacion faltante', u'El periodo especificado no fue encontrado')
        period_id = periodObj.browse(cr, uid, period_ids[0])
        if form.xml_target == 'accounts_catalog':
            accountObj = self.pool.get('account.account')
            if account_ids is None:
                account_ids = accountObj.search(cr, uid, [('take_for_xml', '=', True)])
            accounts = accountObj.browse(cr, uid, account_ids)
            ctas = []
            for acc in accounts:
                if not acc.sat_code_id:
                    raise osv.except_osv(u'Informacion faltante', u'La cuenta %s no tiene asociado un codigo agrupador del SAT' % acc.name_get())
                if acc.first_period_id.date_start <= period_id.date_start:
                    ctaAttrs = [('CodAgrup', acc.sat_code_id.key)]
                    ctaAttrs.append(('NumCta', acc.code[0:100]))
                    ctaAttrs.append(('Desc', acc.name[0:400]))
                    if acc.parent_id:
                        ctaAttrs.append(('SubCtaDe', acc.parent_id.code[0:100]))
                    ctaAttrs.append(('Nivel', acc.level + 1 if acc.level else 1))
                    ctaAttrs.append(('Natur', 'A' if acc.in_cred else 'D'))
                    ctas.append(('Ctas', ctaAttrs))

            if not len(ctas):
                raise osv.except_osv(u'Archivo vacio', u'No se encontraron cuentas para XML cuyo primer periodo reportado sea mayor o igual al periodo procesado.')
            xml_content = ('Catalogo', [('Version', '1.1'),
              ('RFC', user.company_id.rfc),
              ('Mes', period_id.date_start[5:7]),
              ('Anio', period_id.date_start[0:4]),
              ('unroot', ctas)])
            filename = 'catalogo_cuentas_'
            catalog_ns = self._SAT_NS.copy()
            catalog_ns['catalogocuentas'] = self._ACCOUNTS_CATALOG_URI
            xmlTree = self._xml_from_dict(xml_content, catalog_ns, self._ACCOUNTS_CATALOG_URI)
            xmlTree.attrib['{{{pre}}}schemaLocation'.format(pre=self._XSI_DECLARATION)] = 'http://www.sat.gob.mx/esquemas/ContabilidadE/1_1/CatalogoCuentas/CatalogoCuentas_1_1.xsd'
        elif form.xml_target == 'trial_balance':
            if balance_ids is None:
                trialWizardObj = self.pool.get('account.monthly_balance_wizard')
                trial_balance_id = trialWizardObj.create(cr, uid, {'chart_account_id': form.accounts_chart.id,
                 'company_id': user.company_id.id,
                 'period_id': period_id.id,
                 'partner_breakdown': False})
                balance_ids = eval(trialWizardObj.get_info(cr, uid, [trial_balance_id])['domain'][1:-1])[2]
            balanceRecords = self.pool.get('account.monthly_balance').browse(cr, uid, balance_ids)
            ctas = []
            for record in balanceRecords:
                if record.account_id.take_for_xml and record.account_id.first_period_id.date_start <= period_id.date_start:
                    ctasAttrs = []
                    ctasAttrs.append(('NumCta', record.account_code[0:100]))
                    ctasAttrs.append(('SaldoIni', round(record.initial_balance, 2)))
                    ctasAttrs.append(('Debe', round(record.debit, 2)))
                    ctasAttrs.append(('Haber', round(record.credit, 2)))
                    ctasAttrs.append(('SaldoFin', round(record.ending_balance, 2)))
                    ctas.append(('Ctas', ctasAttrs))

            if not len(ctas):
                raise osv.except_osv(u'Archivo vacio', u'Ninguna cuenta de la balanza en este periodo esta marcada para considerarse en el XML.')
            filename = 'balanza_comprobacion_'
            content = [('Version', '1.1'),
             ('RFC', user.company_id.rfc),
             ('Mes', period_id.date_start[5:7]),
             ('Anio', period_id.date_start[0:4]),
             ('TipoEnvio', form.trial_delivery),
             ('unroot', ctas)]
            if form.trial_delivery == 'C':
                content.append(('FechaModBal', form.trial_lastchange_date))
            trialBalance_ns = self._SAT_NS.copy()
            trialBalance_ns['BCE'] = self._TRIAL_BALANCE_URI
            xmlTree = self._xml_from_dict(('Balanza', content), trialBalance_ns, self._TRIAL_BALANCE_URI)
            xmlTree.attrib['{{{pre}}}schemaLocation'.format(pre=self._XSI_DECLARATION)] = 'http://www.sat.gob.mx/esquemas/ContabilidadE/1_1/BalanzaComprobacion/BalanzaComprobacion_1_1.xsd'
        elif form.xml_target in ('vouchers', 'helpers'):
            if form.request_type in ('AF', 'FC'):
                if len(form.order_number) != 13:
                    raise osv.except_osv(u'Numero de orden erroneo', u'Verifique que su numero de orden contenga 13 caracteres (incluida la diagonal)')
                if not re.compile('[A-Z]{3}[0-6][0-9][0-9]{5}(/)[0-9]{2}').match(form.order_number.upper()):
                    raise osv.except_osv(u'Numero de orden erroneo', u'Verifique que su numero de orden tenga la siguiente estructura:\n  ' + u'  * Tres letras mayusculas de la A al Z sin incluir la "Ñ"\n' + u'  * Un digito entre 0 y 6\n' + u'  * Un digito entre 0 y 9\n' + u'  * Cinco digitos entre 0 y 9\n' + u'  * Una diagonal "/"\n' + u'  * Dos digitos del entre 0 y 9')
            if form.request_type in ('DE', 'CO'):
                if len(form.procedure_number) != 10 or not re.compile('[0-9]{10}').match(form.procedure_number):
                    raise osv.except_osv(u'Numero de tramite erroneo', u'Verifique que su numero de tramite contenga 10 digitos.')
            accountMoveObj = self.pool.get('account.move')
            if moveIds is None:
                moveIds = accountMoveObj.search(cr, uid, [('period_id', '=', period_id.id), ('state', '=', 'posted')])
            moves = accountMoveObj.browse(cr, uid, moveIds)
            if not len(moves):
                raise osv.except_osv(u'Informacion faltante', u'No se han encontrado polizas para el periodo seleccionado.')
            entries = []
            if form.xml_target == 'vouchers':
                for mv in moves:
                    voucher = (mv.ref if mv.ref else '') + '(' + mv.name + ')'
                    if not len(mv.line_id):
                        raise osv.except_osv(u'Poliza incompleta', u'La poliza %s no tiene asientos definidos.' % voucher)
                    if not mv.item_concept:
                        raise osv.except_osv(u'Informacion faltante', u'La poliza %s no tiene definido un concepto' % voucher)
                    mvAttrs = [('NumUnIdenPol', mv.name[0:50]), ('Fecha', mv.date), ('Concepto', mv.item_concept[0:300])]
                    lines = []
                    for ln in mv.line_id:
                        if not ln.name:
                            raise osv.except_osv(u'Informacion faltante', u'Compruebe que todos los asientos de la poliza %s tengan un concepto definido.' % voucher)
                        lnAttrs = []
                        lnAttrs.append(('NumCta', ln.account_id.code[0:100]))
                        lnAttrs.append(('DesCta', ln.account_id.name[0:100]))
                        lnAttrs.append(('Concepto', ln.name[0:200]))
                        lnAttrs.append(('Debe', round(ln.debit, 2)))
                        lnAttrs.append(('Haber', round(ln.credit, 2)))
                        (cfdis, others, foreigns, checks, transfers, payments,) = ([],
                         [],
                         [],
                         [],
                         [],
                         [])
                        for cmpl in ln.complement_line_ids:
                            if cmpl.rfc and not _RFC_PATTERN.match(cmpl.rfc):
                                raise osv.except_osv(u'Informacion incorrecta', u'El RFC "%s" no es valido con respecto a los lineamientos del SAT. Poliza %s' % (cmpl.rfc, voucher))
                            if cmpl.rfc2 and not _RFC_PATTERN.match(cmpl.rfc2):
                                raise osv.except_osv(u'Informacion incorrecta', u'El RFC "%s" no es valido con respecto a los lineamientos del SAT. Poliza %s' % (cmpl.rfc2, voucher))
                            cmpl_attrs = []
                            commons = ['cfdi', 'foreign', 'other']
                            cmpl_attrs.append(('MontoTotal' if cmpl.type_key in commons else 'Monto', round(cmpl.amount, 2)))
                            if cmpl.compl_currency_id:
                                if not cmpl.compl_currency_id.sat_currency_id:
                                    raise osv.except_osv(u'Informacion faltante', u'La moneda "%s" no tiene asignado un codigo del SAT.' % cmpl.compl_currency_id.name)
                                cmpl_attrs.append(('Moneda', cmpl.compl_currency_id.sat_currency_id.code))
                            if cmpl.exchange_rate:
                                cmpl_attrs.append(('TipCamb', round(cmpl.exchange_rate, 5)))
                            commons.pop(1)
                            commons.append('check')
                            commons.append('transfer')
                            if cmpl.type_key in commons:
                                if cmpl.rfc and cmpl.rfc2 and cmpl.rfc != user.company_id.rfc and cmpl.rfc2 != user.company_id.rfc:
                                    cmpl_attrs.append(('RFC', cmpl.rfc2.upper()))
                                else:
                                    cmpl_attrs.append(('RFC', cmpl.rfc.upper() if cmpl.rfc != user.company_id.rfc else cmpl.rfc2.upper()))
                            commons.pop(0)
                            commons.pop(0)
                            if cmpl.type_key in commons:
                                cmpl_attrs.append(('CtaOri', cmpl.origin_native_accid.acc_number[0:50] if cmpl.show_native_accs else cmpl.origin_account_id.code[0:50]))
                            commons.append('payment')
                            if cmpl.type_key in commons:
                                cmpl_attrs.append(('Fecha', cmpl.compl_date))
                                cmpl_attrs.append(('Benef', cmpl.payee_acc_id.name[0:300] if cmpl.show_native_accs2 else cmpl.payee_id.name[0:300]))
                            if cmpl.type_key == 'cfdi':
                                if cmpl.uuid:
                                    if len(cmpl.uuid) != 36 or not _UUID_PATTERN.match(cmpl.uuid.upper()):
                                        raise osv.except_osv(u'Informacion incorrecta', u'El UUID "%s" en la poliza %s no se apega a los lineamientos del SAT.' % (cmpl.uuid, voucher))
                                    cmpl_attrs.append(('UUID_CFDI', cmpl.uuid.upper()))
                                cfdis.append(('CompNal', cmpl_attrs))
                            elif cmpl.type_key == 'other':
                                if cmpl.cbb_series and not _SERIES_PATTERN.match(cmpl.cbb_series):
                                    raise osv.except_osv(u'Informacion incorrecta', u'La "Serie" en el comprobante de la poliza %s solo debe contener letras.' % voucher)
                                if cmpl.cbb_series:
                                    cmpl_attrs.append(('CFD_CBB_Serie', cmpl.cbb_series))
                                cmpl_attrs.append(('CFD_CBB_NumFol', cmpl.cbb_number))
                                others.append(('CompNalOtr', cmpl_attrs))
                            elif cmpl.type_key == 'foreign':
                                cmpl_attrs.append(('NumFactExt', cmpl.foreign_invoice))
                                cmpl_attrs.append(('TaxID', cmpl.foreign_taxid))
                                foreigns.append(('CompExt', cmpl_attrs))
                            elif cmpl.type_key == 'check':
                                cmpl_attrs.append(('Num', cmpl.check_number))
                                cmpl_attrs.append(('BanEmisNal', cmpl.origin_bank_id.sat_bank_id.bic))
                                if cmpl.origin_bank_id.sat_bank_id.bic == '999':
                                    cmpl_attrs.append(('BanEmisExt', cmpl.origin_frgn_bank))
                                checks.append(('Cheque', cmpl_attrs))
                            elif cmpl.type_key == 'transfer':
                                cmpl_attrs.append(('BancoOriNal', cmpl.origin_bank_id.sat_bank_id.bic))
                                if cmpl.origin_bank_id.sat_bank_id.bic == '999':
                                    cmpl_attrs.append(('BancoOriExt', cmpl.origin_bank_id.name[0:150]))
                                cmpl_attrs.append(('CtaDest', cmpl.destiny_native_accid.acc_number[0:50] if cmpl.show_native_accs1 else cmpl.destiny_account_id.code[0:50]))
                                cmpl_attrs.append(('BancoDestNal', cmpl.destiny_bank_id.sat_bank_id.bic))
                                if cmpl.destiny_bank_id.sat_bank_id.bic == '999':
                                    cmpl_attrs.append(('BancoDestExt', cmpl.destiny_frgn_bank))
                                transfers.append(('Transferencia', cmpl_attrs))
                            elif cmpl.type_key == 'payment':
                                cmpl_attrs.append(('MetPagoPol', cmpl.pay_method_id.code))
                                cmpl_attrs.append(('RFC', cmpl.rfc2.upper()))
                                payments.append(('OtrMetodoPago', cmpl_attrs))

                        if len(cfdis):
                            lnAttrs.append(('unroot', cfdis))
                        if len(others):
                            lnAttrs.append(('unroot', others))
                        if len(foreigns):
                            lnAttrs.append(('unroot', foreigns))
                        if len(checks):
                            lnAttrs.append(('unroot', checks))
                        if len(transfers):
                            lnAttrs.append(('unroot', transfers))
                        if len(payments):
                            lnAttrs.append(('unroot', payments))
                        lines.append(('Transaccion', lnAttrs))

                    mvAttrs.append(('unroot', lines))
                    entries.append(('Poliza', mvAttrs))

            else:
                for mv in moves:
                    if not len(mv.complement_line_ids):
                        continue
                    voucher = (mv.ref if mv.ref else '') + '(' + mv.name + ')'
                    if not mv.name or mv.name == '/':
                        raise osv.except_osv(u'Informacion faltante', u'La poliza %s no tiene un numero definido.' % voucher)
                    if not mv.date:
                        raise osv.except_osv(u'Informacion faltante', u'La poliza %s no tiene una fecha definida.' % voucher)
                    mvAttrs = [('NumUnIdenPol', mv.name), ('Fecha', mv.date)]
                    (cfdis, others, foreigns,) = ([], [], [])
                    for cmpl in mv.complement_line_ids:
                        cmpl_attrs = [('MontoTotal', round(cmpl.amount, 2))]
                        if cmpl.rfc:
                            if not _RFC_PATTERN.match(cmpl.rfc):
                                raise osv.except_osv(u'Informacion incorrecta', u'El RFC "%s" no es valido con respecto a los lineamientos del SAT. Poiza %s' % (cmpl.rfc, voucher))
                            cmpl_attrs.append(('RFC', cmpl.rfc))
                        if cmpl.compl_currency_id:
                            if not cmpl.compl_currency_id.sat_currency_id:
                                raise osv.except_osv(u'Informacion faltante', u'La moneda "%s" no tiene asignado un codigo del SAT.' % cmpl.compl_currency_id.name)
                            cmpl_attrs.append(('Moneda', cmpl.compl_currency_id.sat_currency_id.code))
                        if cmpl.exchange_rate:
                            cmpl_attrs.append(('TipCamb', round(cmpl.exchange_rate, 5)))
                        if cmpl.pay_method_id:
                            cmpl_attrs.append(('MetPagoAux', cmpl.pay_method_id.code))
                        if cmpl.type_key == 'cfdi':
                            if cmpl.uuid:
                                if len(cmpl.uuid) != 36 or not _UUID_PATTERN.match(cmpl.uuid.upper()):
                                    raise osv.except_osv(u'Informacion incorrecta', u'El UUID "%s" en la poliza %s no se apega a los lineamientos del SAT.' % (cmpl.uuid, voucher))
                            cmpl_attrs.append(('UUID_CFDI', cmpl.uuid.upper()))
                            cfdis.append(('ComprNal', cmpl_attrs))
                        elif cmpl.type_key == 'other':
                            if cmpl.cbb_series:
                                cmpl_attrs.append(('CFD_CBB_Serie', cmpl.cbb_series))
                            cmpl_attrs.append(('CFD_CBB_NumFol', cmpl.cbb_number))
                            others.append(('ComprNalOtr', cmpl_attrs))
                        else:
                            if cmpl.foreign_taxid:
                                cmpl_attrs.append(('TaxID', cmpl.foreign_taxid))
                            cmpl_attrs.append(('NumFactExt', cmpl.foreign_invoice))
                            foreigns.append(('ComprExt', cmpl_attrs))

                    if len(cfdis):
                        mvAttrs.append(('unroot', cfdis))
                    if len(others):
                        mvAttrs.append(('unroot', others))
                    if len(foreigns):
                        mvAttrs.append(('unroot', foreigns))
                    entries.append(('DetAuxFol', mvAttrs))

                if not len(entries):
                    raise osv.except_osv(u'Auxiliar vacio', u'No se encontraron polizas que tengan complementos auxiliares relacionados.')
            content = [('Version', '1.1' if form.xml_target == 'vouchers' else '1.2'),
             ('RFC', user.company_id.rfc),
             ('Mes', period_id.date_start[5:7]),
             ('Anio', period_id.date_start[0:4]),
             ('TipoSolicitud', form.request_type),
             ('unroot', entries)]
            if form.request_type in ('AF', 'FC'):
                content.append(('NumOrden', form.order_number.upper()))
            if form.request_type in ('DE', 'CO'):
                content.append(('NumTramite', form.procedure_number))
            target_ns = self._SAT_NS.copy()
            if form.xml_target == 'vouchers':
                filename = 'polizas_'
                target_ns['PLZ'] = self._VOUCHERS_URI
                xmlTree = self._xml_from_dict(('Polizas', content), target_ns, self._VOUCHERS_URI)
                xmlTree.attrib['{{{pre}}}schemaLocation'.format(pre=self._XSI_DECLARATION)] = 'http://www.sat.gob.mx/esquemas/ContabilidadE/1_1/PolizasPeriodo/PolizasPeriodo_1_1.xsd'
            else:
                filename = 'auxiliar_folios_'
            target_ns['RepAux'] = self._HELPERS_URI
            xmlTree = self._xml_from_dict(('RepAuxFol', content), target_ns, self._HELPERS_URI)
            xmlTree.attrib['{{{pre}}}schemaLocation'.format(pre=self._XSI_DECLARATION)] = 'http://www.sat.gob.mx/esquemas/ContabilidadE/1_1/AuxiliarFolios/AuxiliarFolios_1_1.xsd'
        filename += period_id.date_start[5:7] + '_' + period_id.date_start[0:4] + '.xml'
        validationResult = self._validate_xml(cr, uid, form.xml_target + '.xsd', xmlTree, filename)
        if isinstance(validationResult, dict):
            return validationResult
        self.write(cr, uid, ids, {'state': validationResult,
         'filename': filename,
         'primary_file': b64enc(self._outputXml(xmlTree))})
        return self._reopen_wizard(ids[0])

    def do_stamp(self, cr, uid, ids, context):
        form = self.browse(cr, uid, ids)[0]
        stamp_res = 'stamp_done'
        xslt_path = self._find_file_in_addons('asti_eaccounting_mx_base_70/sat_xslt', form.xml_target + '.xslt')
        try:
            xslt_file = open(xslt_path, 'r')
        except:
            raise osv.except_osv('Hoja XSLT no encontrada', u'La hoja de transformacion no fue encontrada en la ruta "%s"' % xslt_path)
        xsltTree = et.parse(xslt_file)
        xsltTree.find('{http://www.w3.org/1999/XSL/Transform}output').attrib['omit-xml-declaration'] = 'yes'
        try:
            xslt = et.XSLT(xsltTree)
        except et.XSLTParseError:
            xsltTree.find('{http://www.w3.org/1999/XSL/Transform}include').attrib['href'] = xslt_path.replace(form.xml_target, 'utils')
            try:
                xslt = et.XSLT(xsltTree)
                stamp_res = 'stamp_xcpt'
            except:
                xslt = None
        if xslt is None:
            raise osv.except_osv('Error al cargar la hoja XSLT', 'Por favor intente sellar de nuevo el documento.')
        xmlTree = et.ElementTree(et.fromstring(b64dec(form.primary_file)))
        transformedDocument = str(xslt(xmlTree))
        user = self.pool.get('res.users').browse(cr, uid, uid)
        allConfiguredCerts = user.company_id._get_current_certificate(cr, uid, [user.company_id.id])
        if user.company_id.id not in allConfiguredCerts.keys() or not allConfiguredCerts[user.company_id.id]:
            raise osv.except_osv(u'Informacion faltante', u'No se ha encontrado una configuracion de certificados disponible para la compania %s' % user.company_id.name)
        eCert = self.pool.get('res.company.facturae.certificate').browse(cr, uid, [allConfiguredCerts[user.company_id.id]])[0]
        if not eCert.certificate_key_file_pem:
            raise osv.except_osv(u'Informacion faltante', 'Se necesita una clave en formato PEM para poder sellar el documento')
        crypter = RSA.load_key_string(b64dec(eCert.certificate_key_file_pem))
        algrthm = MessageDigest('sha1')
        algrthm.update(transformedDocument)
        rawStamp = crypter.sign(algrthm.digest(), 'sha1')
        certHexNum = X509.load_cert_string(b64dec(eCert.certificate_file_pem), X509.FORMAT_PEM).get_serial_number()
        certNum = ('%x' % certHexNum).replace('33', 'B').replace('3', '')
        cert = ''.join([ ln for ln in b64dec(eCert.certificate_file_pem).split('\n') if 'CERTIFICATE' not in ln ])
        target = '{'
        if form.xml_target == 'accounts_catalog':
            target += self._ACCOUNTS_CATALOG_URI + '}Catalogo'
        elif form.xml_target == 'trial_balance':
            target += self._TRIAL_BALANCE_URI + '}Balanza'
        xmlTree.getroot().attrib['Sello'] = b64enc(rawStamp)
        xmlTree.getroot().attrib['noCertificado'] = certNum
        xmlTree.getroot().attrib['Certificado'] = cert
        validationResult = self._validate_xml(cr, uid, form.xml_target + '.xsd', xmlTree, form.filename)
        if isinstance(validationResult, dict):
            return validationResult
        self.write(cr, uid, ids, {'state': stamp_res,
         'stamped_file': b64enc(self._outputXml(xmlTree))})
        return self._reopen_wizard(ids[0])

    def do_zip(self, cr, uid, ids, context):
        form = self.browse(cr, uid, ids)[0]
        (descriptor, zipname,) = tempfile.mkstemp('eaccount_', '__asti_')
        zipDoc = ZipFile(zipname, 'w')
        xmlContent = b64dec(form.stamped_file) if form.stamped_file else b64dec(form.primary_file)
        zipDoc.writestr(form.filename, xmlContent, zipfile.ZIP_DEFLATED)
        zipDoc.close()
        os.close(descriptor)
        filename = self.pool.get('res.users').browse(cr, uid, uid).company_id.rfc + str(form.year) + form.month
        if form.xml_target == 'accounts_catalog':
            filename += 'CT'
        elif form.xml_target == 'trial_balance':
            filename += 'B' + form.trial_delivery
        elif form.xml_target == 'vouchers':
            filename += 'PL'
        elif form.xml_target == 'helpers':
            filename += 'XF'
        filename += '.zip'
        self.write(cr, uid, ids, {'state': 'zip_done',
         'zipped_file': b64enc(open(zipname, 'rb').read()),
         'filename': filename})
        return self._reopen_wizard(ids[0])

files_generator_wizard()
