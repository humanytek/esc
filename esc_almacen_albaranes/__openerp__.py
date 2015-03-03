# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Humanytek (<http://humanytek.com>).
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
    'name': 'HMTK Stock Customization',
    'version': '0.1',
    'sequence': 1,
    'category': 'Custom',
    'complexity': "easy",
    'description': """ This module is used to add some field and report for 
    Import Information Packing original package""",
    'author': 'Humanytek',
    'website': 'http://humanytek.com',
    'depends': [
        'base',
        'stock',
        'esc_almacen_configuracion',
        'esc_almacen_trazabilidad'
    ],
    'data': [
        # Seguridad y grupos
        
        # Data
        
        # View y menu
        'view/albaranes_stock_move_view.xml',   # Para: Entrada, Internos y Salida
        'view/albaranes.xml',                   # Para: Entrada, Internos y Salida
        'view/albaranes_entrada.xml',
        'view/albaranes_internos.xml',
        'view/albaranes_salida.xml',
        
        # Reportes
        'report/albaranes_entrada.xml',
        'report/albaranes_internos.xml',
        'report/albaranes_salida.xml'
    ],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
