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
import base64

class xsdvalidation_handler_wizard(osv.osv_memory):
    _name = 'xsdvalidation.handler.wizard'
    _columns = {'error_filename': fields.char('Error filename', size=20, required=True),
     'error_file': fields.binary('Detalles del error'),
     'sample_xmlname': fields.char('Sample XML Name', size=128, required=True),
     'sample_xml': fields.binary('XML con validacion fallida')}

xsdvalidation_handler_wizard()
