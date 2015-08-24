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
    'name': 'HMTK Almacén/Trazabilidad',
    'version': '0.1',
    'sequence': 1,
    'category': 'Custom',
    'complexity': "easy",
    'description': """
Módulo de Almacén, desarrollos realizados en submenú Trazabilidad.

Detalles:
---------
* Cambios en Control de Pedimentos
    * Cambiar etiqueta de menú "Import informaction packing" por "Control de pedimentos"
    * Cambiar etiqueta "Número de operación" por "Número de pedimento"
    * Cambiar "Personalizados" por "Aduana", crear el modelo de aduana, crear un grupo editor para aduana
    * Ocultar campo "Proveedor"
    * Cambiar la etiqueta "Fecha" por "Fecha de pedimento"

* Cambios en Números de lote
    * Ocultar campo Fecha de fin de vida
    * Ocultar fecha de eliminación
    * Hacer obligatorios "Fecha de caducidad" y "Fecha de alerta", cambiar etiqueta "Fecha de alerta" por "Fecha de retest"

* Menú Almacén/Trazabilidad/Certificado de análisis
    """,
    'author': 'Humanytek',
    'website': 'http://humanytek.com',
    'depends': [
        'base',
        'stock',
        'l10n_mx_import_info',
        'hmtk_l10n_mx_import_info_custom',
        'product_import_cert',
        'esc_almacen_configuracion',        
    ],
    'data': [
        # Seguridad y grupos
        'security/ir.model.access.csv',
    
        # Data
        
        # Vistas
        'view/numeros_lote.xml',
        'view/control_pedimentos.xml',
        'view/certificados_importacion.xml',
        'view/cert_analisis.xml',
        
        # Reportes
        'report/cert_analisis.xml'
    ],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
