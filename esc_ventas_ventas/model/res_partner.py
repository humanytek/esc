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
import logging
_logger = logging.getLogger(__name__)

class res_partner_esc(osv.Model):

    _inherit = 'res.partner'
    _description = 'Personalizacion para datos del cliente'
    
    # 15/06/2015 (felix) Metodo original modificado
    def _fields_sync(self, cr, uid, partner, update_values, context=None):
        """ Sync commercial fields and address fields from company and to children after create/update,
        just as if those were all modeled as fields.related to the parent """
        # 1. From UPSTREAM: sync from parent
        if update_values.get('parent_id') or update_values.get('use_parent_address'):
            # 1a. Commercial fields: sync if parent changed
            if update_values.get('parent_id'):
                self._commercial_sync_from_company(cr, uid, partner, context=context)
            # 1b. Address fields: sync if parent or use_parent changed *and* both are now set 
            if partner.parent_id and partner.use_parent_address:
                onchange_vals = self.onchange_address(cr, uid, [partner.id],
                                    use_parent_address=partner.use_parent_address,
                                    parent_id=partner.parent_id.id,
                                    context=context).get('value', {})
                partner.update_address(onchange_vals)

        # 2. To DOWNSTREAM: sync children 
        if partner.child_ids:
            # 2a. Commercial Fields: sync if commercial entity
            if partner.commercial_partner_id == partner:
                commercial_fields = self._commercial_fields(cr, uid, context=context)
                if any(field in update_values for field in commercial_fields):
                    self._commercial_sync_to_children(cr, uid, partner, context=context)
            # 2b. Address fields: sync if address changed
            address_fields = self._address_fields(cr, uid, context=context)
            if any(field in update_values for field in address_fields):
                domain_children = [('parent_id', '=', partner.id), ('use_parent_address', '=', True)]
                update_ids = self.search(cr, uid, domain_children, context=context)
                self.update_address(cr, uid, update_ids, update_values, context=context)
                
        # Sincronizar desde el padre el campo "Perfiles"
        if partner.answers_ids:
            domain_children = [('parent_id', '=', partner.id)]
            update_ids = self.search(cr, uid, domain_children, context=context)
            for c in update_ids:
                contacto = self.browse(cr, uid, c, context)
                valores = []
                for perfil in partner.answers_ids:
                    valores.append({perfil.id: perfil.question_id.id})
                for campos in valores:
                    self.write(cr, uid, [contacto.id], {'answers_ids': [(6, 0, campos)]}, context)
    
res_partner_esc()
