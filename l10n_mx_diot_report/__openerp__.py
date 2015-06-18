# -*- encoding: utf-8 -*-
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
    "name" : "MEXICO - DIOT Report",
    "version" : "1.1",
    "author" : "SF Soluciones",
    "category" : "Generic Modules",
    "description": """Module DIOT for  Mexico
    
    The modules 
    - account_move_line_base_tax
    - account_voucher_tax
    are in lp:addons-vauxoo/7.0
    
    If you have old moves without this modules installed, and the company have
    configurated the tax by 'purchase' and by 'sales', you can use the wizard 
    account_update_amount_tax_in_move_lines located in lp:addons-vauxoo/7.0
    to update this moves
    """,
    "website" : "sfsoluciones.com",
    "license" : "AGPL-3",
    "depends" : [
        "base_vat",
        "account_move_line_base_tax",
        "account_accountant",
        "l10n_mx_account_invoice_tax",
        "l10n_mx_account_tax_category",
        "l10n_mx_base_vat_split",
        "account_voucher_tax",
        ],
    "demo" : [],
    "data" : [
        "partner_view.xml",
        "wizard/wizard_diot_report_view.xml",
    ],
    'js': [],
    'qweb' : [],
    'css':[],
    'test': [],
    "installable" : True,
    "active" : False,
}
