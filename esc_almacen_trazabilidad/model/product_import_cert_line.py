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

from openerp.osv import fields, osv
from openerp.tools.translate import _
from datetime import *
import logging
_logger = logging.getLogger(__name__)


class product_import_certificate_line_esc(osv.Model):

    _name = 'product.import.certificate.line'
    _description = 'Creacion modelo Certificados de analisis'
    _columns = {
        'name': fields.char('Pais', size=250),
        'cod_pais': fields.char('Codigo de pais', size=250),
        'moneda_id': fields.many2one('res.currency', 'Moneda'),
        'certificado_id': fields.many2one('product.import.certificate',
            'Certificado de importacion')
    }
    
product_import_certificate_line_esc()
