# -*- encoding: utf-8 -*-
###########################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#
#    Copyright (c) 2011 Vauxoo - http://www.vauxoo.com
#    All Rights Reserved.
#    Info (info@vauxoo.com)
############################################################################
#    Coded by: isaac (isaac@vauxoo.com)
#    Coded by: moylop260 (moylop260@vauxoo.com)
#    Financed by: http://www.sfsoluciones.com (aef@sfsoluciones.com)
############################################################################
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
from osv import osv
from osv import fields
from tools.translate import _
import netsvc
import base64

class print_zebra_memory_wizard_report(osv.osv_memory):
    
    _name = 'print.zebra.memory.wizard.report'
    _description= 'Print zebra memory wizard report'
    _columns = {
        'label.zpl': fields.binary('Print', readonly=True),
    }
    
    _defaults = {
        'label.zpl': lambda self, cr, uid, context=None: context and context.get('label.zpl', False),
    }
    
print_zebra_memory_wizard_report()


class print_zebra_memory_wizard(osv.osv_memory):

    _name = 'print.zebra.memory.wizard'
    _description= 'Print zebra memory wizard'
    _columns = {
        'company_id': fields.many2one('res.company', 'Company', required=True),
        'product_info_ids':fields.one2many('print.zebra.memory.lines.wizard', 
            'memory_id','Lineas etiquetas'),
    }
    _defaults = {
        'company_id': lambda self, cr, uid, context=None: self.pool.get('res.company').browse(cr, uid, uid, context=context).id,
    }
    
    def check_report(self, cr, uid, ids, context=None):
    
        mod_obj = self.pool.get('ir.model.data')

        if context is None:
            context = {}
        data = self.read(cr, uid, ids, [], context=context)[0]
        model_data_ids = mod_obj.search(cr, uid, [('model','=','ir.ui.view'),('name','=','view_print_zebra_memory_wizard_report_form')], context=context)
        resource_id = mod_obj.read(cr, uid, model_data_ids, fields=['res_id'], context=context)[0]['res_id']
        
        service = netsvc.LocalService('report.label.report.import.info.lines.zpl')
        data = self.read(cr, uid, ids)[0]
        (result, format) = service.create(cr, uid, [data['id']], {'model': 'print.zebra.memory.wizard', 'form': data}, {})
        
        context.update({'label.zpl': base64.encodestring(result or '')})
        return {
            'name': _('Report'),
            'view_type': 'form',
            'context': context,
            'view_mode': 'tree,form',
            'res_model': 'print.zebra.memory.wizard.report',
            'views': [(resource_id,'form')],
            'type': 'ir.actions.act_window',
            'target': 'new',
            'nodestroy': True
        }
    
    def ____________check_report(self, cr, uid, ids, context=None):
        service = netsvc.LocalService('report.label.report.import.info.lines.zpl')
        data = self.read(cr, uid, ids)[0]
        (result, format) = service.create(cr, uid, [data['id']], {'model': 'print.zebra.memory.wizard', 'form': data}, {})
        return {
            'value': {'company_id': False},
            'warning':  {'title':'Success', 'message':'some usefull info'},
        }
        
print_zebra_memory_wizard()


class print_zebra_memory_lines_wizard(osv.osv_memory):
    
    _name = 'print.zebra.memory.lines.wizard'
    _description= 'Print zebra memory lines wizard'

    def onchange_product_id(self, cr, uid, ids, product_id, product_uom_id):
        res={}
        res= {
            'value':{
                'product_uom_id': product_id and self.pool.get('product.product').browse(cr, uid, product_id).uom_id.id or False,
                'supplier_id': product_id and self._get_supplier(cr, uid, ids, product_id) or False,
            }
        }
        return res

    def _get_supplier(self, cr, uid, ids, prod_id):
        if prod_id:
            query="""
                select b.id, name from product_product a
                inner join product_supplierinfo b
                on b.product_id=a.product_tmpl_id
                where a.id=%s
                order by b.sequence
                limit 1 offset 0
            """%(prod_id)
            cr.execute( query )
            res = cr.dictfetchall()
            supplier_id = res and res[0]['name'] or False
            return supplier_id

    _columns = {
        'memory_id':fields.many2one('print.zebra.memory.wizard', 'Memory id'),
        'product_id':fields.many2one('product.product', 'Producto', required = True),
        'import_info_id':fields.many2one('import.info', 'Importacion'),
        'product_qty':fields.float('Cantidad', required= True),
        'product_uom_id':fields.many2one('product.uom', 'UOM', required = True),
        'supplier_id':fields.many2one('res.partner', 'Supplier', )
    }

    _defaults = {
        'product_qty': 1,
    }

print_zebra_memory_lines_wizard()

