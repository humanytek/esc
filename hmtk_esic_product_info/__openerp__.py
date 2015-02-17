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
{
    'name': 'HMTK ESIC Product Information',
    'version': '0.01',
    'sequence': 1,
    'category': 'Custom',
    'complexity': "easy",
    'description': """ This module is for adding some additional features in Product menu
    1. New page "Features"
    2. New page "product Documentation"
    3. New groups (Product Atributes User & Product Atributes Manager)
    4. In Products list view, added a group by attribute for Manufacturer(field from the module Product Manufacturer)  
    """,
    'author': 'Humanytek',
    'website': 'http://www.humanytek.com',
    'depends': [ 'product','product_manufacturer', 'stock', 'purchase'],
    'data': ['security/security.xml',
             'security/ir.model.access.csv',
             'product_sequence.xml',
             'product_view.xml'],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: