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

class product_tarrif_fraction_esc(osv.Model):

    _inherit = 'product.tarrif_fraction'
    _description = 'Add fields and methods for Tarrif Fraction'
    _columns = {
        'notes': fields.text('Notes'),
        'tax_purchase_id': fields.many2one('account.tax', 'Purchase tax'),
        'tax_import_id': fields.many2one('account.tax', 'Import tax'),
    }
    
product_tarrif_fraction_esc()
