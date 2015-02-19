# -*- coding: utf-8 -*-

import time
from openerp.report import report_sxw

# 26/01/2015 (grb) Metodo para exportar rml y crear PDF
class ordende_pedido(report_sxw.rml_parse):
    def __init__(self, cr, uid, name, context):
        super(ordende_pedido, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
        })

report_sxw.report_sxw(
    'report.imprimir.reporte',
    'sale.order',
    'tylus_reporte/report/ordendepedido.sxw',
    parser=ordende_pedido
)

