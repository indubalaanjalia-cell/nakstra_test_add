from odoo import models, fields, api
import math
import base64
from io import BytesIO
from odoo.tools import barcode as barcode_tool


class ProductLabel(models.Model):
    _name = 'product.label'
    _description = 'Product Label'
    _rec_name = 'label_name'

    label_name = fields.Char(required=True)

    product_id = fields.Many2one(
        'product.product',
        ondelete='cascade'
    )
    product_tmpl_id = fields.Many2one(
        'product.template',
        string="Product",
    )
    sale_purity_id = fields.Many2one('gold.purity', string="Sale Purity")
    sale_price_per_gram = fields.Float(string="Sale Rate / gram")


    diamond_certificate = fields.Binary(
        string="Diamond Certificate",
        attachment=True
    )
    diamond_certificate_filename = fields.Char(
        string="Certificate File Name"
    )
    sale_gross_weight = fields.Float(string="Sale Gross Weight (g)")
    sale_stone_weight = fields.Float(string="Sale Stone Weight (g)")
    sale_diamond_weight = fields.Float(string="Sale Diamond Weight (g)")

    sale_net_weight = fields.Float(
        string="Sale Net Weight (g)",
        compute="_compute_sale_net_weight",
        store=True
    )

    sale_metal_rate = fields.Float(string="Sale Metal Amount")
    sale_stone_rate = fields.Float(string="Sale Stone Amount")
    sale_diamond_rate = fields.Float(string="Sale Diamond Amount")

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
    purity_id = fields.Many2one('gold.purity', string="Purity")
    purchase_price_per_gram = fields.Float(string="Purchase fine Rate / gram")

    purchase_gross_weight = fields.Float(string="Purchase Gross Amount (g)")
    purchase_stone_weight = fields.Float(string="Purchase Stone Weight (g)")
    purchase_diamond_weight = fields.Float(string="Purchase Diamond Weight (g)")

    purchase_net_weight = fields.Float(
        string="Purchase Net Weight (g)",
        compute="_compute_purchase_net_weight",
        store=True
    )

    purchase_metal_rate = fields.Float(string="Purchase Metal Amount")
    purchase_stone_rate = fields.Float(string="Purchase Stone Amount")
    purchase_diamond_rate = fields.Float(string="Purchase Diamond Amount")

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
    mc_fine =fields.Float(string="MC Fine")
    barcode = fields.Char(
        'Barcode', copy=False, index='btree_not_null',
        help="International Article Number used for product identification.")
    tag_weight = fields.Float(string="Tag Weight (g)")
    sale_fine_weight = fields.Float(string="Fine Weight  (g)",compute="_compute_sale_fine_weight")
    purchase_fine_weight = fields.Float(string="Fine Weight  (g)",compute="_compute_purchase_fine_weight",)

    sale_diamond_weight_gm = fields.Float(
        string="Diamond Weight (g)",
        digits=(12, 4)
    )

    sale_diamond_weight_ct = fields.Float(
        string="Diamond Weight (ct)",
        digits=(12, 4)
    )
    purchase_diamond_weight_gm = fields.Float(
        string="Diamond Weight (g)",
        digits=(12, 4)
    )

    purchase_diamond_weight_ct = fields.Float(
        string="Diamond Weight (ct)",
        digits=(12, 4)
    )

    @api.onchange('sale_diamond_weight_ct')
    def _onchange_sale_diamond_weight_ct(self):
        if self.sale_diamond_weight_ct:
            self.sale_diamond_weight_gm = self.sale_diamond_weight_ct * 0.2
        else:
            self.sale_diamond_weight_gm = 0.0

    @api.onchange('sale_diamond_weight_gm')
    def _onchange_sale_diamond_weight_gm(self):
        if self.sale_diamond_weight_gm:
            self.sale_diamond_weight_ct = self.sale_diamond_weight_gm / 0.2
        else:
            self.sale_diamond_weight_ct = 0.0

    @api.onchange('purchase_diamond_weight_ct')
    def _onchange_purchase_diamond_weight_ct(self):
        if self.purchase_diamond_weight_ct:
            self.purchase_diamond_weight_gm = self.purchase_diamond_weight_ct * 0.2
        else:
            self.purchase_diamond_weight_gm = 0.0

    @api.onchange('purchase_diamond_weight_gm')
    def _onchange_purchase_diamond_weight_gm(self):
        if self.purchase_diamond_weight_gm:
            self.purchase_diamond_weight_ct = self.purchase_diamond_weight_gm / 0.2
        else:
            self.purchase_diamond_weight_ct = 0.0

    # =========================
    # COMPUTES
    # =========================
    @api.depends(
        'sale_gross_weight',
        'sale_stone_weight',
        'sale_diamond_weight_gm'
    )
    def _compute_sale_net_weight(self):
        for rec in self:
            rec.sale_net_weight = (
                    rec.sale_gross_weight
                    - rec.sale_stone_weight
                    - rec.sale_diamond_weight_gm
            )
            # rec.sale_net_weight = rec.sale_net_weight*rec.purity_id.percentage

    @api.depends('sale_net_weight','purity_id')
    def _compute_sale_fine_weight(self):
        for rec in self:
            rec.sale_fine_weight = rec.sale_net_weight * (rec.purity_id.percentage)/100

    @api.depends(
        'purchase_gross_weight',
        'purchase_stone_weight',
        'purchase_diamond_weight_gm',
    )
    def _compute_purchase_net_weight(self):
        for rec in self:
            rec.purchase_net_weight = (
                    rec.purchase_gross_weight
                    - rec.purchase_stone_weight
                    - rec.purchase_diamond_weight_gm
            )

    @api.depends('purchase_net_weight','purity_id')
    def _compute_purchase_fine_weight(self):
        for rec in self:
            rec.purchase_fine_weight = rec.purchase_net_weight * (rec.purity_id.percentage)/100

    @api.depends('purchase_net_weight', 'purity_id')
    def _compute_purchase_fine_weight(self):
        for rec in self:
            rec.purchase_fine_weight = rec.purchase_net_weight * (rec.purity_id.percentage) / 100


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

    @api.onchange('product_id')
    def _onchange_product_id_set_template(self):
        for rec in self:
            if rec.product_id:
                rec.product_tmpl_id = rec.product_id.product_tmpl_id
            else:
                rec.product_tmpl_id = False

    @api.onchange('product_tmpl_id')
    def _onchange_product_tmpl_id_set_template(self):
        for rec in self:
            if rec.product_tmpl_id:
                rec.product_id = rec.product_tmpl_id
            else:
                rec.product_id = False

    @api.model
    def create(self, vals):
        """Function to add EAN13 Standard barcode at the time
        create new product"""
        res = super(ProductLabel, self).create(vals)
        ean = generate_ean(str(res.id))
        res.barcode = '21' + ean[2:]
        return res

def ean_checksum(eancode):
    """Returns the checksum of an ean string of length 13, returns -1 if
    the string has the wrong length"""
    if len(eancode) != 13:
        return -1
    odd_sum = 0
    even_sum = 0
    for rec in range(len(eancode[::-1][1:])):
        if rec % 2 == 0:
            odd_sum += int(eancode[::-1][1:][rec])
        else:
            even_sum += int(eancode[::-1][1:][rec])
    total = (odd_sum * 3) + even_sum
    return int(10 - math.ceil(total % 10.0)) % 10


def check_ean(eancode):
    """Returns True if ean code is a valid ean13 string, or null"""
    if not eancode:
        return True
    if len(eancode) != 13:
        return False
    try:
        int(eancode)
    except:
        return False
    return ean_checksum(eancode)


def generate_ean(ean):
    """Creates and returns a valid ean13 from an invalid one"""
    if not ean:
        return "0000000000000"
    product_identifier = '00000000000' + ean
    ean = product_identifier[-11:]
    check_number = check_ean(ean + '00')
    return f'{ean}0{check_number}'


