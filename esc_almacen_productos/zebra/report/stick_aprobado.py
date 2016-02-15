# -*- encoding: utf-8 -*-
import time
import pooler
from report import report_sxw
from tools.translate import _

class esc_zebra_print(report_sxw.rml_parse):

    def __init__(self, cr, user, name, context):
        super(esc_zebra_print, self).__init__(cr, user, name, context=context)
        self.localcontext.update({
            'time': time,
            #'obtiene_ids': self._obtiene_ids,
            #'obtiene_lineas': self._obtiene_lineas,
            #'get_direccion': self._get_direccion,
        })
    """
    def _obtiene_lineas(self, lineas_prod):
        lineas_prod_obj = self.pool.get('print.zebra.memory.lines.wizard')
        lineas_prod_brw = lineas_prod_obj.browse(self.cr, self.uid, lineas_prod)
        return lineas_prod_brw

    def _obtiene_ids(self, product_info_ids):
        lineas_obj = self.pool.get('print.zebra.memory.wizard')
        lineas_brw = lineas_obj.browse(self.cr, self.uid, [product_info_ids])
        return lineas_brw

    def _get_direccion(self,parter_id):
        if parter_id:
            partner_address_obj = self.pool.get('res.partner.address')
            partner_obj = self.pool.get('res.partner')
            id_address = partner_address_obj.search(self.cr, self.uid, [('partner_id', '=', parter_id), ('type', '=', 'default') ])
            address_brw = partner_address_obj.browse(self.cr, self.uid, id_address)[0]
            return address_brw
        else:
            return False
    """

report_sxw.report_sxw(
    'report.zebra.stick.aprobado',
    #'print.zebra.memory.wizard',
    'esc_almacen_productos/zebra/report/stick_aprobado.rml',
    parser=esc_zebra_print
)

