from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # =========================
    # SALES JEWELLERY DETAILS
    # =========================
    sale_purity_id = fields.Many2one('gold.purity', string="Sale Purity")
    sale_price_per_gram = fields.Float(string="Sale Rate / gram")

    sale_gross_weight = fields.Float(string="Sale Gross Weight (g)")
    sale_stone_weight = fields.Float(string="Sale Stone Weight (g)")
    sale_diamond_weight = fields.Float(string="Sale Diamond Weight (g)")

    sale_net_weight = fields.Float(
        string="Sale Net Weight (g)",
        compute="_compute_sale_net_weight",
        store=True
    )

    sale_metal_rate = fields.Float(string="Sale Metal Rate")
    sale_stone_rate = fields.Float(string="Sale Stone Rate")
    sale_diamond_rate = fields.Float(string="Sale Diamond Rate")

    sale_making_charge_type = fields.Selection([
        ('percent', 'Percentage'),
        ('amount', 'Amount')
    ], string="Sale Making Charge Type", default='percent')

    sale_making_charge_value = fields.Float(string="Sale Making Charge")

    sale_making_charge_amount = fields.Float(
        string="Sale Making Charge Amount",
        compute="_compute_sale_making_charge",
        store=True
    )

    # =========================
    # PURCHASE JEWELLERY DETAILS
    # =========================
    purchase_purity_id = fields.Many2one('gold.purity', string="Purchase Purity")
    purchase_price_per_gram = fields.Float(string="Purchase Rate / gram")

    purchase_gross_weight = fields.Float(string="Purchase Gross Weight (g)")
    purchase_stone_weight = fields.Float(string="Purchase Stone Weight (g)")
    purchase_diamond_weight = fields.Float(string="Purchase Diamond Weight (g)")

    purchase_net_weight = fields.Float(
        string="Purchase Net Weight (g)",
        compute="_compute_purchase_net_weight",
        store=True
    )

    purchase_metal_rate = fields.Float(string="Purchase Metal Rate")
    purchase_stone_rate = fields.Float(string="Purchase Stone Rate")
    purchase_diamond_rate = fields.Float(string="Purchase Diamond Rate")

    purchase_making_charge_type = fields.Selection([
        ('percent', 'Percentage'),
        ('amount', 'Amount')
    ], string="Purchase Making Charge Type", default='percent')

    purchase_making_charge_value = fields.Float(string="Purchase Making Charge")

    purchase_making_charge_amount = fields.Float(
        string="Purchase Making Charge Amount",
        compute="_compute_purchase_making_charge",
        store=True
    )

    # =========================
    # COMPUTES
    # =========================
    @api.depends(
        'sale_gross_weight',
        'sale_stone_weight',
        'sale_diamond_weight'
    )
    def _compute_sale_net_weight(self):
        for rec in self:
            rec.sale_net_weight = (
                rec.sale_gross_weight
                - rec.sale_stone_weight
                - rec.sale_diamond_weight
            )

    @api.depends(
        'purchase_gross_weight',
        'purchase_stone_weight',
        'purchase_diamond_weight'
    )
    def _compute_purchase_net_weight(self):
        for rec in self:
            rec.purchase_net_weight = (
                rec.purchase_gross_weight
                - rec.purchase_stone_weight
                - rec.purchase_diamond_weight
            )

    @api.depends(
        'sale_making_charge_type',
        'sale_making_charge_value',
        'sale_net_weight',
        'sale_metal_rate'
    )
    def _compute_sale_making_charge(self):
        for rec in self:
            if rec.sale_making_charge_type == 'percent':
                rec.sale_making_charge_amount = (
                    rec.sale_net_weight * rec.sale_metal_rate
                ) * (rec.sale_making_charge_value / 100)
            else:
                rec.sale_making_charge_amount = rec.sale_making_charge_value

    @api.depends(
        'purchase_making_charge_type',
        'purchase_making_charge_value',
        'purchase_net_weight',
        'purchase_metal_rate'
    )
    def _compute_purchase_making_charge(self):
        for rec in self:
            if rec.purchase_making_charge_type == 'percent':
                rec.purchase_making_charge_amount = (
                    rec.purchase_net_weight * rec.purchase_metal_rate
                ) * (rec.purchase_making_charge_value / 100)
            else:
                rec.purchase_making_charge_amount = rec.purchase_making_charge_value

