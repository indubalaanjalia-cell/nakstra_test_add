from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    label_id = fields.Many2one(
        'product.label',
        string="Label",
    )