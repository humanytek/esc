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
from hashlib import sha1

class company_fit(osv.osv):
    _inherit = 'res.company'
    _columns = {'regname': fields.char('Razon social', size=250, required=True),
     'rfc': fields.char('R.F.C.', size=15, required=True),
     'ext_num': fields.char('Num. ext', size=50),
     'int_num': fields.char('Num. int', size=50),
     'mobile_number': fields.char('Movil', size=50),
     'locality': fields.char('Localidad', size=200),
     'block': fields.char('Colonia', size=200),
     'accounts_config_done': fields.boolean('Accounts config done'),
     'license_key': fields.char('Clave de licenciamiento', size=40),
     'apply_in_check': fields.boolean('Cheque'),
     'apply_in_trans': fields.boolean('Transferencia'),
     'apply_in_cfdi': fields.boolean('Comp. nacional'),
     'apply_in_other': fields.boolean('Comp. otro'),
     'apply_in_forgn': fields.boolean('Comp. extranjero'),
     'apply_in_paymth': fields.boolean('Metodo de pago')}
    _defaults = {'regname': '',
     'rfc': ''}

    def _check_validity(self, cr, uid, ids, request = None):
        records = self.browse(cr, uid, ids)
        target = records[0] if len(records) else records
        if not target.name or not target.regname or not target.rfc:
            is_invalid = True
        else:
            val = u'ASTI-eAccounting' + target.name + (target.street if target.street else u'') + target.regname + target.rfc + u'-V1.1'
            is_invalid = sha1(val.encode('UTF-8')).hexdigest().lower() != target.license_key.lower() if target.license_key else True
        if request is None:
            return is_invalid
        if is_invalid:
            request['arch'] = '<form string="" version="7"><separator string="La licencia de uso no es valida"/><h4>Compruebe que los campos "Nombre", "Razon social" y "R.F.C." de la compania esten correctamente configurados.</h4><h4>Ha cambiado sus datos de empresa recientemente?</h4></form>'
        return request

company_fit()
