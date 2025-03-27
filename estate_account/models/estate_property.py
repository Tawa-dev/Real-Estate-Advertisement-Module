from odoo import models, Command

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def action_sold(self):
        # create invoice for the sold property
        for property in self:
            # create the invoice
            invoice = self.env['account.move'].create({
                'partner_id': property.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    # 6% commision line
                    Command.create({
                        'name': f'Commission for {property.name}',
                        'quantity': 1,
                        'price_unit': property.selling_price * 0.06,
                    }),
                    # adminstrative fees line
                    Command.create({
                        'name': 'Adminstrative fees',
                        'quantity': 1,
                        'price_unit': 100.0
                    })
                ]
            })
        # call the original method
        return super().action_sold()
