from odoo import models, fields, api


class GoldRateMaster(models.Model):
    _name = 'gold.rate.master'
    _description = 'Gold Rate Master'
    _order = 'date desc'

    name = fields.Char(
        string='Reference',
        compute='_compute_name',
        store=True
    )

    date = fields.Date(
        string='Rate Date',
        required=True,
        default=fields.Date.context_today
    )

    rate_per_gram = fields.Float(
        string='Gold Rate / Gram',
        required=True
    )

    board_rate = fields.Float(
        string='Board Rate',
        required=True
    )

    active = fields.Boolean(
        string='Active',
        default=False
    )

    @api.depends('date', 'rate_per_gram')
    def _compute_name(self):
        for rec in self:
            rec.name = f"Gold Rate {rec.date} - {rec.rate_per_gram}"


    def action_set_active_rate(self):
        self.ensure_one()
        self.search([('id', '!=', self.id)]).write({'active': False})
        self.active = True

