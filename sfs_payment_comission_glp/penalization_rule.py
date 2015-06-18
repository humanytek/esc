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

from osv import osv, fields

class penalization_rule(osv.osv):
    _name = 'penalization.rule'
    _descritpion = 'Model To define penalization rules'
    _columns = {
                'name': fields.char('Name', size=64),
                'active': fields.boolean('Active'),
                'rule_line_ids': fields.one2many('penalization.rule.line', 'penalization_id',
                                                 'Penalization Rules')
                }
    _defaults = {
                 'active': True
                 }
penalization_rule()

class penalization_rule_line(osv.osv):
    _name = 'penalization.rule.line'
    _description = 'Model to define the rule lines'
    _columns = {
                'qty': fields.integer('Quantity'),
                'penelization_percent': fields.float('Penalization %'),
                'penalization_id': fields.many2one('penalization.rule', 'Penalization', ondelete='cascade')
                }
penalization_rule_line()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
