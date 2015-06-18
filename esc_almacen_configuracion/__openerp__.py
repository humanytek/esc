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
    'name': 'HMTK Almacén/Configuración',
    'version': '0.1',
    'sequence': 1,
    'category': 'Stock',
    'complexity': "easy",
    'description': """
Este módulo proporciona el desarrollo y cambios en las configuraciones para el módulo de Almacén (stock).

* Creación menú Almacén/Configuración/Aduanas
* Creación grupo para permisos de usuarios administrativos de los registros de aduanas
* Creación menú Almacén/Configuración/Condiciones para Albaranes de pre-entrada
* Creación menú Almacén/Configuración/Pruebas certificados de análisis
    """,
    'author': 'Humanytek',
    'website': 'http://humanytek.com',
    'depends': [
        'base',
        'stock',
        'l10n_mx_import_info',
        'hmtk_l10n_mx_import_info_custom'
    ],
    'data': [
        # Seguridad y grupos
        'security/aduana_group.xml',
        
        # Data
        'data/aduanas_data.xml',
        
        # View y menu
        'view/configuracion_aduanas.xml',
        'view/configuracion_condiciones.xml',
        'view/configuracion_cert_test.xml',
        
        # Reportes
        
    ],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
