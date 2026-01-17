from odoo import models, fields


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    purity_id = fields.Many2one('gold.purity', string="Purity")
    fine_weight = fields.Float(string="Fine Weight  (g)")
    mc_amount =fields.Float(string="MC Amount")



