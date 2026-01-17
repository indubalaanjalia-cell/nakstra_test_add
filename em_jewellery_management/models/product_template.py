from odoo import models, fields, api, _
import math

from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # =========================
    # SALES JEWELLERY DETAILS
    # =========================
    sale_purity_id = fields.Many2one('gold.purity', string="Sale Purity")
    sale_price_per_gram = fields.Float(string="Sale Rate / gram")
    is_scheme_product = fields.Boolean(string="Scheme Product")

    label_count = fields.Integer(
        string="Labels",
        compute="_compute_label_count"
    )

    def _compute_label_count(self):
        Label = self.env['product.label']
        for template in self:
            template.label_count = Label.search_count([
                ('product_tmpl_id', '=', template.id)
            ])

    def action_view_labels(self):
        self.ensure_one()
        return {
            'name': 'Product Labels',
            'type': 'ir.actions.act_window',
            'res_model': 'product.label',
            'view_mode': 'tree,form',
            'domain': [('product_tmpl_id', '=', self.id)],
            'context': {
                'default_product_tmpl_id': self.id,
            },
        }

    @api.constrains('is_scheme_product')
    def _check_single_scheme_product(self):
        for product in self:
            if product.is_scheme_product:
                count = self.search_count([
                    ('is_scheme_product', '=', True),
                    ('id', '!=', product.id),
                ])
                if count:
                    raise ValidationError(
                        _("Only ONE product can be marked as Scheme Product.")
                    )


class Product(models.Model):
    _inherit = 'product.product'

    is_scheme_product = fields.Boolean(string="Scheme Product")
    sale_purity_id = fields.Many2one(
        'gold.purity',
        string="Sale Purity"
    )

    sale_price_per_gram = fields.Float(
        string="Sale Rate / gram"
    )

    label_count = fields.Integer(
        string="Labels",
        compute="_compute_label_count"
    )

    def _compute_label_count(self):
        Label = self.env['product.label']
        for product in self:
            product.label_count = Label.search_count([
                ('product_tmpl_id', '=', product.product_tmpl_id.id)
            ])

    def action_view_labels(self):
        self.ensure_one()
        return {
            'name': 'Product Labels',
            'type': 'ir.actions.act_window',
            'res_model': 'product.label',
            'view_mode': 'tree,form',
            'domain': [('product_tmpl_id', '=', self.product_tmpl_id.id)],
            'context': {
                'default_product_tmpl_id': self.product_tmpl_id.id,
            },
        }

    @api.constrains('is_scheme_product')
    def _check_single_scheme_product(self):
        for product in self:
            if product.is_scheme_product:
                count = self.search_count([
                    ('is_scheme_product', '=', True),
                    ('id', '!=', product.id),
                ])
                if count:
                    raise ValidationError(
                        _("Only ONE product can be marked as Scheme Product.")
                    )






