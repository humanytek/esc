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
    'name': 'HMTK Ventas/Ventas',
    'version': '0.1',
    'sequence': 1,
    'category': 'Custom',
    'complexity': 'easy',
    'description': """
Módulo de Ventas, modificado para cubrir requerimientos de ESIC.

Detalles:
---------
* Cambios en submenú Ventas/Ventas/Cotizaciones
    * Agregar un campo "Fecha de entrega" por cada línea de salida
    * Agregar un campo "Fecha de pedido" en el form principal

* Cambios en submenú Ventas/Ventas/Pedidos de ventas
    * Agregar un campo "Código y nombre de producto según el cliente"
    * Agregar campo de "Perfiles" en formulario y en la impresión de reporte
    * Desglose de entrega de productos
    """,
    'author': 'Humanytek',
    'website': 'http://humanytek.com',
    'depends': [
        'base',
        'sale'
    ],
    'data': [
        # Seguridad y grupos
    
        # Data
        
        # Vistas
        'view/cotizaciones.xml',
        'view/pedidos_ventas.xml',
        
        # Reportes
        'report/sale_report.xml'
    ],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
