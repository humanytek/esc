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
class import_info_custom(osv.Model):
    _name = 'import.info.custom'
    _rec_name = 'custom_name'
    _columns = {
        'custom_name': fields.char('Custom Name', size=128, required=True),
        'custom number': fields.char('Custom Number', size=6, required=True),
        }
import_info_custom()   

class import_info(osv.Model):
    _inherit = 'import.info'
    _columns = {
        'customs': fields.many2one('import.info.custom', 'Customs')
        }
import_info()
<<<<<<< HEAD
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
=======
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
>>>>>>> cb4962fad3142e8e0b527bc62ab8e02abcbec558
