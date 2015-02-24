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

class account_journal_types(osv.osv):
    _name = 'account.journal.types'
    _description = 'Objeto para los tipos de polizas'
    _columns = {'name': fields.char('Nombre', size=120, required=True),
     'code': fields.char('Codigo', size=20, required=True)}

    def create(self, cr, uid, vals, context):
        if 'allow_management' not in context or not context['allow_management']:
            raise osv.except_osv('Operacion no definida', 'Los tipos de poliza no pueden ser creados manualmente.')
        return super(account_journal_types, self).create(cr, uid, vals, context)

    def write(self, cr, uid, ids, vals, context):
        if 'allow_management' not in context or not context['allow_management']:
            raise osv.except_osv('Operacion no definida', 'Los tipos de poliza no pueden ser modificados manualmente.')
        return super(account_journal_types, self).write(cr, uid, ids, vals, context)

    def unlink(self, cr, uid, ids, context):
        if 'allow_management' not in context or not context['allow_management']:
            raise osv.except_osv('Operacion no definida', 'Los tipos de poliza no pueden ser eliminados manualmente.')
        return super(account_journal_types, self).unlink(cr, uid, context)

account_journal_types()
