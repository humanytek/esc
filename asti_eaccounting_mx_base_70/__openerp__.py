##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2010-2015 Humanytek SAPI de CV (<http://www.humanytek.com>). 
#    All Rights Reserved
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
    'name' : 'Contabilidad electrónica para México',
    'description' : """Adecuación para cumplir con los requisitos de la Contabilidad Electrónica
         promulgada en 2014. Este módulo añade puntos específicos requeridos para generar los documentos
         XML requeridos por SAT, a saber:
         * Administración del código agrupador de SAT para las cuentas fiscales.
         * Definición de un código agrupador para cada cuenta fiscal.
         * Campos de moneda y tipo de cambio para el detalle general de los asientos contables.
         * Pestañas para detalle de cheques, transferencias y CFDI en el detalle de los asientos contables.
         * Tipo de cuenta (acreedora/deudora).
         * Simplificación en los registros de cuentas bancarias (clientes, proveedores y empresa).
         * Administración de tipos de pólizas.
         * Definición de un tipo de póliza para cada diario contable.
         * Campo de moneda para los registros de cliente y proveedores.
         * Simplificación de los registros de bancos.
         * Campos de dirección para los registros de compañía.
         * Cuentas bancarias para los registros de compañía.
         """,
    'version' : '1.0',
    'author' : 'Humanytek',
    'website' : 'http://www.humanytek.com',
    'license' : 'GPL-3',
    'category' : 'Accounting',
    'depends' : ['base', 'account', 'account_cancel', 'hesatec_mx_accounting_reports_v7'],
    'init_xml' : [],
    'update_xml' : ['eaccount_sat_code_view.xml',
                    'eaccount_journal_type_view.xml',
                    'eaccount_bank_view.xml',
                    'account_fit_view.xml',
                    'eaccount_account_bank_view.xml',
                    'company_fit_view.xml',
                    'journal_fit_view.xml',
                    'eaccount_currency_view.xml',
                    'account_moveline_fit_view.xml',
                    'hesa_filegenerate_view.xml',
                    'eaccount_payment_methods_view.xml',
                    'account_move_fit_view.xml',
                    'wizard/files_generator_view.xml',
                    'wizard/overall_config_view.xml',
                    'wizard/movelines_info_manager_view.xml',
                    'wizard/xsdvalidation_handler_view.xml',
                    'security/groups.xml',
                    'security/ir.model.access.csv',
                    'loadable_data/complements.xml',
                    'restrictive_actions.xml',
                    'menu.xml'],
    'demo_xml' : [],
    'installable' : 'True',
    'auto_install' : False
}
