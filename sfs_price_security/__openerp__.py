# -*- encoding: utf-8 -*
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
    'name': 'Price Security',
    'version': '1.1',
    'category': 'Sales Management ',
    'description': """ 
         Permission to edit the field "price_unit" on sale.order.line model.
    """,
    'author': 'SF Soluciones' ,
    'website': 'sfsoluciones.com' ,
    'depends': ['sale'] ,
    'init_xml': [],
    'update_xml': [
                   'security/price_security.xml',
                   'sale_order_line_view.xml'
                  ] ,
    'demo_xml': [] ,
    'test': [] ,
    'installable': True , 
    'active': False ,
    'certificate': '' ,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:-