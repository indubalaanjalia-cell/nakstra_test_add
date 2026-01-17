from odoo import models, fields,api,_
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    old_gold_po_ids = fields.One2many(
        'purchase.order',
        'sale_id',
        string='Old Gold Purchase Orders'
    )

    old_gold_po_count = fields.Integer(
        compute='_compute_old_gold_po_count'
    )
    apply_scheme = fields.Boolean(string="Apply Scheme")
    scheme_line_id = fields.Many2one(
        'sale.order.line',
        string="Scheme Line",
        readonly=True,
        copy=False
    )

    def _compute_old_gold_po_count(self):
        for order in self:
            order.old_gold_po_count = len(order.old_gold_po_ids)


    def action_create_old_gold_po(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Old Gold Purchase',
            'res_model': 'purchase.order',
            'view_mode': 'form',
            'context': {
                'default_partner_id': self.partner_id.id,
                'default_sale_id': self.id,
                'default_is_old_gold': True,
            },
        }

    def action_open_old_gold_pos(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Old Gold Purchases',
            'res_model': 'purchase.order',
            'view_mode': 'tree,form',
            'domain': [('sale_id', '=', self.id), ('is_old_gold', '=', True)],
        }

    def _get_customer_scheme_records(self):
        self.ensure_one()
        return self.env['customer.scheme'].search([
            ('partner_id', '=', self.partner_id.id),
            ('state', '=', 'posted'),
            ('remaining_amount', '>', 0),
        ], order='id')

    def _get_customer_scheme_amount(self):
        self.ensure_one()
        schemes = self._get_customer_scheme_records()
        return sum(schemes.mapped('remaining_amount'))

    def _get_scheme_product(self):
        product = self.env['product.product'].search(
            [('is_scheme_product', '=', True)],
            limit=1
        )
        if not product:
            raise UserError(_("Please configure a Scheme Product first."))
        return product

    def action_apply_scheme(self):
        for order in self:
            if not order.partner_id:
                raise UserError(_("Select customer first."))

            schemes = order._get_customer_scheme_records()
            total_available = sum(schemes.mapped('remaining_amount'))

            if not total_available:
                raise UserError(_("No scheme balance available."))

            scheme_product = order._get_scheme_product()

            consume_amount = min(total_available, order.amount_untaxed)

            # Create scheme sale line
            line = self.env['sale.order.line'].create({
                'order_id': order.id,
                'product_id': scheme_product.id,
                'product_uom_qty': 1,
                'product_uom': scheme_product.uom_id.id,
                'price_unit': -consume_amount,
                'name': scheme_product.name,
            })

            # 🔥 CONSUME scheme balance (FIFO)
            remaining = consume_amount
            for scheme in schemes:
                if remaining <= 0:
                    break

                if scheme.remaining_amount <= remaining:
                    remaining -= scheme.remaining_amount
                    scheme.remaining_amount = 0
                else:
                    scheme.remaining_amount -= remaining
                    remaining = 0

            order.scheme_line_id = line

    def action_remove_scheme(self):
        for order in self:

            consumed_amount = abs(order.scheme_line_id.price_unit)

            # Restore scheme balance (reverse FIFO)
            schemes = self.env['customer.scheme'].search([
                ('partner_id', '=', order.partner_id.id),
                ('state', '=', 'posted'),
            ], order='id desc')

            remaining = consumed_amount
            for scheme in schemes:
                if remaining <= 0:
                    break

                restoreable = scheme.scheme_amount - scheme.remaining_amount
                restore = min(restoreable, remaining)
                scheme.remaining_amount += restore
                remaining -= restore

            order.scheme_line_id.unlink()
            order.scheme_line_id = False




