from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    sale_id = fields.Many2one(
        'sale.order',
        string='Related Sale Order'
    )

    is_old_gold = fields.Boolean(
        string='Old Gold Purchase',
        default=False
    )
