from odoo import models, fields, api
import math


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # =========================
    # SALES JEWELLERY DETAILS
    # =========================
    sale_purity_id = fields.Many2one('gold.purity', string="Sale Purity")
    sale_price_per_gram = fields.Float(string="Sale Rate / gram")

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




