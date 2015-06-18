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
    'name': 'HMTK Compras/Compra',
    'version': '0.1',
    'sequence': 1,
    'category': 'Custom',
    'complexity': 'easy',
    'description': """
En este modulo, se agregan desarrollos y vistas del modulo de compras (purchase), especificamente relacionados con el menu Compras/Compra

Detalles:
---------
* Flujo secundario en la vista Pedidos de compra
* Solapa de preguntas por cada Etapa de pedidos de compra en la vista Pedidos de compra
* Formulario de gestion y grupo administrativo para flujo secundario; Compras/Configuración/Compra/Etapas de pedidos de compra
* Solapa instrucciones de embarque
* Creación de filtro por etapas secundaria (Flujo secundario)
    """,
    'author': 'Humanytek',
    'website': 'http://humanytek.com',
    'depends': [
        'base',
        'purchase',
        'hmtk_esic_product_info',
        'esc_almacen_trazabilidad',
        'l10n_mx_cities',
        'product_import_cert'
    ],
    'data': [
        # Seguridad y grupos
        'security/etapas_group.xml',
    
        # Data
        
        # Vistas
        'view/pedidos_compra.xml',
        'view/proveedores.xml',
        'view/configuracion.xml',
        'view/pedidos_compra_config.xml',
        
        # Reportes
        'report/pedidos_compra.xml',
    ],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
