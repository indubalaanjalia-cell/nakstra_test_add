from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'


    is_job_worker = fields.Boolean(string='Job Worker')
    default_making_charge = fields.Float(string='Making Charge / Gram')
    show_making_charge = fields.Boolean(compute='_compute_show_making_charge')
    scheme_amount = fields.Monetary(
        string='Scheme Balance',
        currency_field='currency_id',
        default=0.0
    )

    @api.depends('is_job_worker')
    def _compute_show_making_charge(self):
        for rec in self:
            rec.show_making_charge = rec.is_job_worker

    @api.depends('is_job_worker')
    def _compute_show_making_charge(self):
        for rec in self:
            rec.show_making_charge = rec.is_job_worker