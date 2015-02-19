# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2014 ZestyBeanz Technologies Pvt. Ltd.
#    (http://wwww.zbeanztech.com)
#    contact@zbeanztech.com
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
    'name': 'Product Quantity On Hand',
    'version': '1.0.1',
    'category': 'Sales Management',
    'summary': 'Product Quantity On Hand',
    'description': """ 
        This module adds a function to PostgreSQL Database which can be used to get the Quantity on hand of the product through sql query
            * Usage : SELECT get_qty_onhand(<product_id>);
            * Example : SELECT get_qty_onhand(1234);
    """,
    'author': 'SF Soluciones',
    'website': 'sfsoluciones.com',
    'depends': ['sale', 'stock'],
    'data': ['security/ir.model.access.csv',
             'account_move_line_view.xml'
                   ],
    'demo': [],
    'test': [],
    'installable': True,
    'active': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
