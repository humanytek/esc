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
import re
import logging
_logger = logging.getLogger(__name__)

class purchase_stage_esc(osv.Model):

    _name = 'purchase.stage'
    _description = 'Campos y metodos para el modulo de compras, etapas de flujo'
    
    # 04/03/2015 (felix) Generar la secuencia consecutiva
    def _get_secuencia(self, cr, uid, context=None):
        sec = 0
        all_stage = self.search(cr, uid, [(1, '=', 1)], order='secuencia')
        if not all_stage:
            sec = 1
        for i in self.browse(cr, uid, all_stage, context):
            sec = i.secuencia + 1
        return sec
       
    _columns = {
        'name': fields.char('Nombre de etapa', size=250),
        'secuencia': fields.integer('Secuencia'),
        'activa': fields.boolean('Activada'),
        'campos_ids': fields.one2many('purchase.stage.line', 'campos_id', 
            'Campos administrados'),
        'purchase_stage_ids': fields.one2many('purchase.order', 
            'purchase_stage_id', 'Etapas pedidos de compra'),
    }
    _order = 'secuencia asc'
    _defaults = {
        'secuencia': _get_secuencia
    }
    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Este campo debe ser unico')
    ]
    
    # 05/03/2015 (felix) Metodo para guardar registro en purchase.stage e ir.model.fields
    def create(self, cr, uid, vals, context=None):
        if vals['campos_ids']:
            obj_fields = self.pool.get('ir.model.fields')
            for i in vals['campos_ids']:
                values_fields = {}
                values_fields = {
                    'name': i[2]['name'],
                    'field_description': i[2]['field_description'],
                    'state': i[2]['state'],
                    'model_id': i[2]['model_id'],
                    'ttype': i[2]['ttype'],
                    'size': i[2]['size'],
                    'required': i[2]['required'],
                    'readonly': i[2]['readonly'],
                    'select_level': i[2]['select_level'],
                    'on_delete': i[2]['on_delete']
                }
                obj_fields.create(cr, uid, values_fields, context)
        return super(purchase_stage_esc, self).create(cr, uid, vals, context=context)
    
purchase_stage_esc()


class purchase_stage_line_esc(osv.Model):
    '''
    03/03/2015 (felix)
    Esta tabla es para guardar de manera visual en el programa
    campos adicionales para cada etapa del sub-flujo en pedidos de compra
    '''
    _name = 'purchase.stage.line'
    _description = 'Campos para validar en sub-flujo pedidos de compra'
    _columns = {
        'campos_id': fields.many2one('purchase.stage', 'Campos'),
        'name': fields.char('Nombre de campo', size=250),
        'field_description': fields.char('Etiqueta de campo', size=250),
        'state': fields.selection([('manual','Campo personalizado')], 'Tipo'),
        'model_id': fields.many2one('ir.model', 'Modelo', 
            domain=[('model', '=', 'purchase.order')]),
        'ttype': fields.selection([('char', 'Texto corto'),
            ('text', 'Caja de texto'), ('date','Fecha'),
            ('datetime', 'Fecha y hora'), ('boolean', 'Checkbox')], 
            'Tipo de campo'),
        'size': fields.integer('Tamano'),
        'required': fields.boolean('Requerido'),
        'readonly': fields.boolean('Solo lectura'),
        'select_level': fields.selection([('0','No puede ser buscado')], 
            'Objeto de busqueda'),
        'on_delete': fields.selection([('set null','Establecer a NULL')], 
            'Al eliminar')
    }
    _rec_name='field_description'
    _defaults = {
        'name': 'x_',
        'state': lambda self,cr,uid,ctx=None: (ctx and ctx.get('manual',False)) and 'manual' or 'base',
        'select_level': '0',
        'on_delete': 'set null',
        'field_description': '',
    }
    
    # 06/03/2015 (felix) Validacion para que el campo siempre lleve prefijo: x_
    def on_change_name(self, cr, uid, ids, campo, context=None):
        if campo:
            if not re.match('^x_',campo):
                raise osv.except_osv('Advertencia','El nombre de campo debe llevar un prefjio "x_"')
        else:
            raise osv.except_osv('Advertencia','El nombre de campo es obligatorio y debe llevar un prefjio "x_"')
        return {}
    
purchase_stage_line_esc()


class purchase_stage_fields_esc(osv.Model):

    _name = 'purchase.stage.fields'
    _description = 'Preguntas sociadas a las etapas de pedidos de compra'
    _columns = {
        'purchase_stage_id': fields.many2one('purchase.order', 'Preguntas'),
        'name': fields.char('Complemento', size=250)
    }
    
purchase_stage_fields_esc()
