from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    label_id = fields.Many2one(
        'product.label',
        string="Label",
    )
    purity_id = fields.Many2one('gold.purity', string="Purity")
    fine_weight = fields.Float(string="Fine Weight  (g)")
    mc_amount = fields.Float(string="MC Amount")
    tag_weight = fields.Float(string="Tag Weight (g)")
    net_weight = fields.Float(string="Net Weight  (g)")

    @api.onchange('label_id','product_uom_qty','tax_id')
    def _onchange_label_id(self):
        if self.label_id:
            self.purity_id = self.label_id.purity_id.id
            self.fine_weight =self.label_id.sale_fine_weight
            self.mc_amount = self.label_id.sale_making_charge_amount
            self.price_subtotal =(self.product_uom_qty*self.price_unit)+self.mc_amount
            self.price_total =((self.product_uom_qty*self.price_unit)+self.mc_amount)
            self.tag_weight = self.label_id.tag_weight





