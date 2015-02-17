# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2013 SF Soluciones.
#    (http://www.sfsoluciones.com)
#    contacto@sfsoluciones.com
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

{
    'name': 'Customer Security',
    'version': '1.0',
    'category': ' ',
    'description': """ 
      if permission is given to user then the user can see all res.partner records taking the field user_id 
      from res.partner model, if not, the users can see only assigned customers.
    """,
    'author': 'SF Soluciones' ,
    'website': 'sfsoluciones.com' ,
    'depends': ['sale'] ,
    'init_xml': [],
    'update_xml': [
                   "security/customer_security.xml",
                  ],
    'demo_xml': [] ,
    'test': [] ,
    'installable': True , 
    'active': False ,
    'certificate': '' ,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: