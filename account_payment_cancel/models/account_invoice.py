# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import models, api, _
from odoo.exceptions import ValidationError

class AccountInvoiceInheritance(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def payment_invoice_cancel(self):
        moves = self.env['account.move']
        for inv in self:
            if inv.move_id:
                moves += inv.move_id
            if inv.payment_ids:
                inv.payment_ids.cancel()
        # First, set the invoices as cancelled and detach the move ids
        self.write({'state': 'cancel', 'move_id': False})
        if moves:
            # second, invalidate the move(s)
            moves.button_cancel()
            # delete the move this invoice was pointing to
            # Note that the corresponding move_lines and move_reconciles
            # will be automatically deleted too
            moves.unlink()
        return True
    
