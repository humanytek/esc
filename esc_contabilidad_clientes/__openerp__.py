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
    'name': 'HMTK Contabilidad/Clientes',
    'version': '0.1',
    'sequence': 1,
    'category': 'Custom',
    'complexity': "easy",
    'description': """
Módulo para desarrollos y cambios en menú Contabilidad/Clientes

Detalles:
---------
* Agregar campo "Código y nombre del producto" según el cliente

    """,
    'author': 'Humanytek',
    'website': 'http://humanytek.com',
    'depends': [
        'base',
        'account',
        'l10n_mx_ir_attachment_facturae',
    ],
    'data': [
        # Seguridad y grupos
        
        # Data
        
        # View y menu
        'view/facturas_cliente.xml',
        #'view/attachment_facturae_mx.xml',
        
        # Reportes
        'report/facturas_cliente.xml',
    ],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
