from odoo import models, fields,api,_

class GramRange(models.Model):
    _name = 'gold.gram.range'
    _description = 'Gold Gram Range'
    _order = 'from_gram'

    name = fields.Char(string="Range", compute="_compute_name", store=True)
    from_gram = fields.Float(string="From (g)", required=True)
    to_gram = fields.Float(string="To (g)", required=True)
    active = fields.Boolean(default=True)

    @api.depends('from_gram','to_gram')
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.from_gram} - {rec.to_gram} g"
