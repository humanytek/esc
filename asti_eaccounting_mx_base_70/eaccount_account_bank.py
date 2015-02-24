# -*- coding: utf-8 -*-
# 2015.02.19 19:07:37 CST
from osv import fields, osv

class bank_eaccount(osv.osv):
    _name = 'eaccount.bank.account'
    _description = 'Versi\xc3\xb3n simplificada para cuentas bancarias'
    _columns = {'code': fields.char('No. de cuenta', size=30, required=True),
     'bank_id': fields.many2one('res.bank', 'Banco', required=True),
     'currency_id': fields.many2one('res.currency', 'Moneda'),
     'account_id': fields.many2one('account.account', 'Account id')}

    def name_get(self, cr, uid, ids, context):
        rs = []
        for el in ids:
            element = self.browse(cr, uid, el)
            rs.append((el, '[' + element.code + '] - ' + element.account_id.name + ' / ' + element.bank_id.name))

        return rs



    def name_search(self, cr, uid, name = '', args = None, operator = 'ilike', context = None, limit = 100):
        if args is None:
            args = []
        if context is None:
            context = {}
        args = args[:]
        if not (name == '' and operator == 'ilike'):
            args += ['|',
             '|',
             ('code', 'ilike', name),
             ('bank_id.name', 'ilike', name),
             ('account_id.name', 'ilike', name)]
        ids = self._search(cr, uid, args, limit=limit, context=context, access_rights_uid=uid)
        res = self.name_get(cr, uid, ids, context)
        return res



bank_eaccount()

class partner_bank_fit(osv.osv):
    _inherit = 'res.partner.bank'

    def name_get(self, cr, uid, ids, context = None):
        rs = []
        for el in ids:
            element = self.browse(cr, uid, el)
            rs.append((el, '[' + element.acc_number + '] - ' + element.partner_id.name + ' / ' + element.bank.name))

        return rs



    def name_search(self, cr, uid, name = '', args = None, operator = 'ilike', context = None, limit = 100):
        if args is None:
            args = []
        if context is None:
            context = {}
        args = args[:]
        if not (name == '' and operator == 'ilike'):
            args += ['|',
             '|',
             ('acc_number', 'ilike', name),
             ('bank.name', 'ilike', name),
             ('partner_id.name', 'ilike', name)]
        ids = self._search(cr, uid, args, limit=limit, context=context, access_rights_uid=uid)
        res = self.name_get(cr, uid, ids, context)
        return res



partner_bank_fit()

# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.02.19 19:07:37 CST
