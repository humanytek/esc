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
    'name': 'HMTK Almacén/Productos',
    'version': '0.1',
    'sequence': 1,
    'category': 'Custom',
    'complexity': "easy",
    'description': """
Módulo de Almacén, desarrollos realizados en submenú Productos.

Detalles:
---------
* Agregada pestaña para describir referencia del producto por cada cliente
* Menú "Almacén/Productos/Etiquetas aprobado" para creación de etiquetas de aprobado
* Agregar campos
    * Operaciones
    * Tipo de ventas
    * Línea de product: [Humana|Veterinaria]
    """,
    'author': 'Humanytek',
    'website': 'http://humanytek.com',
    'depends': [
        'base',
        'stock',
        'product',
        'product_manufacturer',
        'hmtk_esic_product_info',
    ],
    'data': [
        # Seguridad y grupos
        'security/product_group.xml',
        'security/ir.model.access.csv',
        
        # Data
        'data/unidades_caducidad.xml',
        
        # Vistas
        'view/productos.xml',
        'view/etiqueta_aprobado.xml',
        'view/product_tarrif_fraction_form.xml',
        'view/therapeutic_action_form.xml',
        
        # Reportes
        'report/stick_aprobado.xml'
    ],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
