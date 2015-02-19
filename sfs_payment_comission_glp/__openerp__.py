# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2014 SF Soluciones.
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
    'name': 'Payment Commission',
    'version': '1.6',
    'category': 'Accounting & Finance',
    'description': """ 
        Module to calculate commission based on sales and date of payment
    """,
    'author': 'SF Soluciones',
    'website': 'sfsoluciones.com',
    'depends': ['account'],
    'data': [
             'security/payment_comission_security.xml',
             'security/ir.model.access.csv',
             'user_transaction_histrory_view.xml',
             'invoice_view.xml',
             'penalization_rule_view.xml',
             'res_partner_view.xml',
             'report/payment_comission_report_view.xml',
             'wizard/payment_comission_wizard_view.xml'
             ],
    'demo': [],
    'test': [],
    'installable': True,
    'active': False,
    'certificate': '',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: