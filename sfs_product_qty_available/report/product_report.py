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

import tools
from osv import  osv
import openerp.addons.decimal_precision as dp

class product_product_report(osv.osv):
    _name = 'product.product.report'
    _auto = False

    def init(self, cr):
        tools.drop_view_if_exists(cr, 'product_product_report')
        cr.execute("""drop function if exists get_qty_onhand(product_id integer);
                   CREATE OR REPLACE FUNCTION get_qty_onhand
                   (x_product_id integer)
                   RETURNS TABLE(qty numeric) AS
                   $BODY$
                   BEGIN
                   return query
                   select round(coalesce(sum(x.product_qty)::numeric, 0.00), 2)
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
                   LANGUAGE 'plpgsql';
                
                   create or replace view product_product_report as (
                       select
                           min(pt.id) as id,
                           pt.id as product_id,
                           (select get_qty_onhand(pt.id)) as qty_available 
                        from product_template as pt
                        group by
                           pt.id
                       );
                   """)

product_product_report()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: