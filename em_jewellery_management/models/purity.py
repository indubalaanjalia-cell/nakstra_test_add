from odoo import models, fields

class GoldPurity(models.Model):
    _name = 'gold.purity'
    _description = 'Gold Purity'

    name = fields.Char(required=True)        # 22K, 18K
    percentage = fields.Float(string="Purity %")
    active = fields.Boolean(default=True)
