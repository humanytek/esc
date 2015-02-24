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

class account_banks(osv.osv):
    _name = 'eaccount.bank'
    _columns = {'name': fields.char('Razon social', size=250, required=True),
     'code': fields.char('Nombre corto', size=250, required=True),
     'bic': fields.char('Clave', size=11, required=True)}

    def name_get(self, cr, uid, ids, context):
        rs = []
        for el in ids:
            element = self.browse(cr, uid, el)
            rs.append((el, '[' + element.bic + '] ' + element.code))

        return rs

    def name_search(self, cr, uid, name = '', args = None, operator = 'ilike', context = None, limit = 100):
        if args is None:
            args = []
        if context is None:
            context = {}
        args = args[:]
        if not (name == '' and operator == 'ilike'):
            args += ['|', ('code', 'ilike', name), ('bic', 'ilike', name)]
        ids = self._search(cr, uid, args, limit=limit, context=context, access_rights_uid=uid)
        res = self.name_get(cr, uid, ids, context)
        return res

    def create(self, cr, uid, vals, context):
        if 'allow_management' not in context or not context['allow_management']:
            raise osv.except_osv('Operacion no definida', 'Los bancos no pueden ser creados manualmente.')
        return super(account_banks, self).create(cr, uid, vals, context)

    def write(self, cr, uid, ids, vals, context):
        if 'allow_management' not in context or not context['allow_management']:
            raise osv.except_osv('Operacion no definida', 'Los bancos no son directamente modificables.')
        return super(account_banks, self).write(cr, uid, ids, vals, context)

    def unlink(self, cr, uid, ids, context):
        if 'allow_management' not in context or not context['allow_management']:
            raise osv.except_osv('Operacion no definida', 'Los bancos no son directamente eliminables.')
        return super(account_banks, self).unlink(cr, uid, ids, context)

account_banks()

class res_bank_sat(osv.osv):
    _inherit = 'res.bank'
    _columns = {'sat_bank_id': fields.many2one('eaccount.bank', 'Codigo del SAT', required=False)}

res_bank_sat()
