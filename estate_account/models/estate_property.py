from odoo import models, Command
from odoo.exceptions import UserError
from odoo import _

class Property(models.Model):
    _inherit = "estate.property"

    def _nothing_to_invoice_error(self):
        msg = _("""There is nothing to invoice!""")
        return UserError(msg)

    def _create_invoice(self, date=None):
        """
        Create the invoice associated to the SO.
        :returns: list of created invoices
        """
        #TODO: Probar seguridad cuando tengamos terminal...
        if not self.env['estate.property'].check_access_rights('create', False):
            try:
                self.check_access_rights('write')
                self.check_access_rule('write')
            except AccessError:
                return self.env['account.move']

        # 1) Create invoices.

        self.ensure_one()
        journal = self.env['account.move'].sudo().with_context(default_move_type='out_invoice')._get_default_journal()
        if not journal:
            raise UserError(_('Please define an accounting sales journal for the company.'))

        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'journal_id': journal.id,  # company comes from the journal
            'invoice_line_ids': [
                Command.create(
                    {
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': (self.selling_price*6)/100
                }),
                Command.create(
                    {
                    'name': "Administrative fees",
                    'quantity': 1,
                    'price_unit': 100
                })
            ],
        }

        if not invoice_vals:
            raise self._nothing_to_invoice_error()

        # 3) Create invoices.
        # Manage the creation of invoices in sudo because a salesperson must be able to generate an invoice from a
        # sale order without "billing" access rights. However, he should not be able to create an invoice from scratch.
        moves = self.env['account.move'].sudo().with_context(default_move_type='out_invoice').create(invoice_vals)

        return moves

    def action_sold(self):
        self._create_invoice()
        return super().action_sold()