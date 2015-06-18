# -*- encoding: utf-8 -*
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

from osv import fields,osv

class product_engine_type(osv.osv):
    
    _name = 'product.engine.type'
    _desc = "Engine Type"
    _columns = {
                'name': fields.char('Name', size=128, required=True)
            }
    
product_engine_type()

class product_brand(osv.osv):
    
    _name = 'product.brand'
    _desc = 'Brand of the Engine/Power plant'
    _columns = {
                'name': fields.char('Name', size=128, required=True),
                'type': fields.selection([('engine','Engine'), ('power_plant', 'Power Plant'), ('refaccion', 'Refaccion')], 'Type', required=True)
            }

product_brand()

class product_charactersitics(osv.osv):
    
    _name = 'product.charactersitics'
    _desc = 'Characteristics of the Engine/Power plant' 
    _columns = {
                'name': fields.char('Name', size=128, required=True),
                'type': fields.selection([('engine','Engine'), ('power_plant', 'Power Plant'),  ('refaccion', 'Refaccion')], 'Type', required=True)
            }
product_charactersitics()

class product_application(osv.osv):
    
    _name = 'product.application'
    _desc = 'product application'
    _columns = {
                'name': fields.char('Name', size=128, required=True),
            }

product_application()

class product_aspirate(osv.osv):
    
     _name = 'product.aspirate'
     _desc = 'product aspirate'
     _columns = {
                'name': fields.char('Name', size=128, required=True),
            }

product_aspirate()

class product_fuel(osv.osv):

    _name = 'product.fuel'
    _desc = 'product fuel'
    _columns = {
                'name': fields.char('Name', size=128, required=True),
            }

product_fuel()

class product_line(osv.osv):
    
      _name = 'product.line'
      _desc = 'product line'
      _columns = {
                'name': fields.char('Name', size=128, required=True),
            }

product_line()

class product_assembly(osv.osv):
    
    _name = 'product.assembly'
    _desc = 'product assembly'
    _columns = {
                'name': fields.char('Name', size=128, required=True),
            }

product_assembly()

class product_quality(osv.osv):

     _name = 'product.quality'
     _desc = 'product quality'
     _columns = {
                'name': fields.char('Name', size=128, required=True),
            }
     
product_quality()

class product_model(osv.osv):
    
    _name = 'product.model'
    _desc = 'product model'
    _columns = {
                'name': fields.char('Name', size=128, required=True),
            }
     
product_model()

class product_transference(osv.osv):
    
    _name = 'product.transference'
    _desc = 'product transference'
    _columns = {
                'name': fields.char('Name', size=128, required=True),
            }

product_transference()

class product_boot(osv.osv):
    
    _name = 'product.boot'
    _desc = 'product boot'
    _columns = {
                'name': fields.char('Name', size=128, required=True),
            }

product_boot()

class product_product(osv.osv):
    
    _inherit = "product.product"
    _columns = {
                'has_charactersitics': fields.boolean("Has Characteristics"),
                'engine': fields.boolean("Engine"),
                'engine_type_id': fields.many2one('product.engine.type', 'Type of engine'),
                'brand_id': fields.many2one('product.brand','Brand'),
                'capacity': fields.char("Capacity", size=128),
                'application_id': fields.many2one('product.application',"Application"),
                'characteristics_id': fields.many2one('product.charactersitics', 'Characteristics'),
                'cylinders': fields.char('Cylinders', size=128),
                'aspirate_id': fields.many2one('product.aspirate', "Aspirate"),
                'fuel_id': fields.many2one('product.fuel', 'Fuel'),
                'power_plant': fields.boolean('Power Plant'),
                'power_characteristics_id': fields.many2one('product.charactersitics', 'Characteristics'),
                'power_brand_id': fields.many2one('product.brand','Brand'),
                'line_id': fields.many2one('product.line', 'Line'),
                'assembly_id': fields.many2one('product.assembly', 'Assembly'),
                'quality_id': fields.many2one('product.quality', 'Quality'),
                'model_id': fields.many2one('product.model', 'Model'),
                'transference_id': fields.many2one('product.transference','Transference'),
                'boot_id': fields.many2one('product.boot', 'Boot'),
                'cont_term': fields.char('Cont/Term', size=128),
                'case': fields.char('Case', size=128),
                'engine_id': fields.many2one('product.product', 'Engine'),
                'engine_name': fields.many2one('product.category', 'Name', readonly=True),
                'cylinders2': fields.char('Cylinders', size=128, readonly=True),
                'brand_id2': fields.many2one('product.brand','Brand', readonly=True),
                'aspirate_id2': fields.many2one('product.aspirate', "Aspirate", readonly=True),
                'capacity2': fields.char("Capacity", size=128, readonly=True),
            }
    
    def onchange_engine(self, cr, uid, ids, engine_id, context=None):
        res = {}
        if engine_id != False:
            engine_rec = self.browse(cr, uid, engine_id, context=context)
            engine_name = engine_rec.categ_id
            res['value'] = {
                            'engine_name':  engine_rec.categ_id.id or False, 
                            'cylinders2': engine_rec.cylinders or False,
                            'brand_id2': engine_rec.brand_id.id or False,
                            'aspirate_id2': engine_rec.aspirate_id.id or False,
                            'capacity2': engine_rec.capacity or False
                            }
        return res
    
    def engine_val(self, cr, uid, ids, val, context=None):
        res = {}
        if val:
           res['value'] = {
                           'power_plant': False
                        } 
        return res
       
    def power_plant_val(self, cr, uid, ids, val, context=None):
        res = {}
        if val:
           res['value'] = {
                           'engine': False
                        } 
        return res
    
product_product()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:-