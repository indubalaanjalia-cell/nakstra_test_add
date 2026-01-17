from odoo import models, fields, api


class JewelleryRefineryOrder(models.Model):
    _name = 'jewellery.refinery.order'
    _description = 'Jewellery Refinery Order'


    name = fields.Char(default=lambda self: self.env['ir.sequence'].next_by_code('jewellery.refinery'),readonly=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    date = fields.Date(default=fields.Date.today)


    old_gold_weight = fields.Float(string='Old Gold Weight (g)', required=True)
    purity_id = fields.Many2one('gold.purity', string="Purity")

    wastage_percent = fields.Float(string='Wastage %', default=2.0)


    net_gold_weight = fields.Float(compute='_compute_net_weight', store=True)


    gold_bar_weight = fields.Float(compute='_compute_gold_bar_weight', store=True)


    state = fields.Selection([
        ('draft', 'Draft'),('melted', 'Melted'),
        ('done', 'Done')], default='draft')

    @api.depends('old_gold_weight', 'wastage_percent')
    def _compute_net_weight(self):
        for rec in self:
            rec.net_gold_weight = rec.old_gold_weight * (1 - rec.wastage_percent / 100)

    @api.depends('net_gold_weight')
    def _compute_gold_bar_weight(self):
        for rec in self:
            rec.gold_bar_weight = rec.net_gold_weight

    def action_melt_gold(self):
        self.ensure_one()
        old_gold = self.env.ref('jewellery_refinery.product_old_gold')
        gold_bar = self.env.ref('jewellery_refinery.product_gold_bar')

        bom = self.env['mrp.bom']._bom_find(gold_bar)
        if not bom:
            raise ValueError('BoM for Gold Bar not found')

        mo = self.env['mrp.production'].create({
            'product_id': gold_bar.id,
            'product_qty': self.gold_bar_weight,
            'bom_id': bom.id,
        })
        mo.action_confirm()
        mo.button_mark_done()

        self.state = 'melted'