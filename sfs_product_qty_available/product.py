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

from osv import osv

class product_product(osv.osv):
    _inherit = 'product.product'
    
    def set_qty_available_function(self, cr, uid, context=None):
        cr.execute("""drop function if exists get_qty_onhand(product_id integer);
                   CREATE OR REPLACE FUNCTION get_qty_onhand
                   (x_product_id integer)
                   RETURNS TABLE(qty float) AS
                   $BODY$
                   BEGIN
                   return query
                   select round(coalesce(sum(x.product_qty)::float, 0.00))
                   from((SELECT
                        coalesce(sum(-m.product_qty * pu.factor / pu2.factor)::float, 0.0) as product_qty
                   FROM
                    stock_move m
                        LEFT JOIN stock_picking p ON (m.picking_id=p.id)
                        LEFT JOIN product_product pp ON (m.product_id=pp.id)
                        LEFT JOIN product_template pt ON (pp.product_tmpl_id=pt.id)
                        LEFT JOIN product_uom pu ON (pt.uom_id=pu.id)
                        LEFT JOIN product_uom pu2 ON (m.product_uom=pu2.id)
                        LEFT JOIN product_uom u ON (m.product_uom=u.id)
                        LEFT JOIN stock_location l ON (m.location_id=l.id)
                        where m.product_id = x_product_id and l.usage = 'internal' and m.state = 'done'
                   GROUP BY
                        m.id, m.product_id, m.product_uom, pt.categ_id, m.location_id,  m.location_dest_id,
                        m.prodlot_id, m.date, m.state, l.usage, m.company_id, pt.uom_id)
                   UNION ALL (
                   SELECT
                   coalesce(sum(m.product_qty * pu.factor / pu2.factor)::decimal, 0.0) as product_qty
                   FROM
                    stock_move m
                        LEFT JOIN stock_picking p ON (m.picking_id=p.id)
                        LEFT JOIN product_product pp ON (m.product_id=pp.id)
                        LEFT JOIN product_template pt ON (pp.product_tmpl_id=pt.id)
                        LEFT JOIN product_uom pu ON (pt.uom_id=pu.id)
                        LEFT JOIN product_uom pu2 ON (m.product_uom=pu2.id)
                        LEFT JOIN product_uom u ON (m.product_uom=u.id)
                        LEFT JOIN stock_location l ON (m.location_dest_id=l.id)
                        where m.product_id = x_product_id and l.usage='internal' and m.state = 'done'
                   GROUP BY
                        m.id, m.product_id, m.product_uom, pt.categ_id, m.location_id, m.location_dest_id,
                        m.prodlot_id, m.date, m.state, l.usage, m.company_id, pt.uom_id
                    ))x;
                   END
                   $BODY$
                   LANGUAGE 'plpgsql';""")
        return True

product_product()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
