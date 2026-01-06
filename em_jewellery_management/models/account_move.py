# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountMove(models.Model):
    _name = 'account.move'
    _inherit = 'account.move'

    job_work_id = fields.Many2one('jewellery.job.work')
