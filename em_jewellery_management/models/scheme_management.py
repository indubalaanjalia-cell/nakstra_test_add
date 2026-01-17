from odoo import models, fields,api
from odoo.exceptions import UserError


class CustomerScheme(models.Model):
    _name = 'customer.scheme'
    _description = 'Customer Saving Scheme'


    name = fields.Char(string='Scheme Name', required=True)
    partner_id = fields.Many2one(
    'res.partner', string='Customer', required=True, ondelete='cascade'
    )
    scheme_amount = fields.Float(string='Scheme Amount', required=True)
    journal_id = fields.Many2one(
        'account.journal',
        domain="[('type', 'in', ('cash', 'bank'))]",
        required=True
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted')
    ], default='draft')
    payment_id = fields.Many2one()
    payment_line_ids = fields.One2many(
        'customer.scheme.payment',
        'scheme_id',
        string='Payments'
    )

    total_paid = fields.Float(
        string="Total Paid",
        compute="_compute_total_paid",
        store=True
    )
    remaining_amount = fields.Float(string="Remaining Amount")

    def action_post(self):
        for rec in self:
            rec.remaining_amount = rec.scheme_amount
            rec.state = 'posted'

    @api.depends('payment_line_ids.amount')
    def _compute_total_paid(self):
        for rec in self:
            rec.total_paid = sum(rec.payment_line_ids.mapped('amount'))

    def action_add_scheme_amount(self):
        for rec in self:
            if rec.scheme_amount <= 0:
                raise UserError("Amount must be greater than zero")

            payment = self.env['account.payment'].create({
                'payment_type': 'inbound',
                'partner_type': 'customer',
                'partner_id': rec.partner_id.id,
                'amount': rec.scheme_amount,
                'journal_id': rec.journal_id.id,
                'date': fields.Date.today(),
                'ref': rec.name,
            })

            payment.action_post()

            rec.payment_id = payment.id
            rec.partner_id.scheme_amount += rec.scheme_amount
            rec.state = 'posted'

    # def action_update_scheme_amount(self):
    #     for rec in self:
    #         if rec.state != 'draft':
    #             continue
    #
    #         partner = rec.partner_id
    #         if not partner:
    #             continue
    #
    #         # Example logic (if you store previous amount)
    #         difference = rec.scheme_amount - rec._origin.scheme_amount
    #         partner.scheme_amount += difference


class CustomerSchemePayment(models.Model):
    _name = 'customer.scheme.payment'
    _description = 'Customer Scheme Payment'
    _order = 'payment_date'

    scheme_id = fields.Many2one(
        'customer.scheme',
        string='Scheme',
        ondelete='cascade',
        required=True
    )

    payment_date = fields.Date(
        string='Payment Date',
        required=True,
        default=fields.Date.context_today
    )

    amount = fields.Float(
        string='Amount',
        required=True
    )

    journal_id = fields.Many2one(
        related='scheme_id.journal_id',
        store=True,
        readonly=True
    )

    state = fields.Selection(
        related='scheme_id.state',
        store=True,
        readonly=True
    )
