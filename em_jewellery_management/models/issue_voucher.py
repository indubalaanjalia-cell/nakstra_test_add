from odoo import models, fields, api


class JewelleryIssueVoucher(models.Model):
    _name = 'jewellery.issue.voucher'
    _description = 'Issue Voucher'

    name = fields.Char(string='Issue Voucher Number', copy=False, readonly=True, default='New')
    job_work_id = fields.Many2one('jewellery.job.work', required=True)
    job_worker_id = fields.Many2one('res.partner', required=True)
    line_ids = fields.One2many('jewellery.issue.voucher.line', 'voucher_id')
    state = fields.Selection([('draft','Draft'),('done','Done')], default='draft')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('jewellery.issue.voucher') or 'New'
        return super().create(vals)


    def action_done(self):
        stock_loc = self.env.ref('stock.stock_location_stock')
        worker_loc = self.env.ref('stock.stock_location_customers')
        for line in self.line_ids:
            self.env['stock.move'].create({
            'name': self.job_work_id.name,
            'product_id': line.product_id.id,
            'product_uom_qty': line.qty,
            'product_uom': line.product_id.uom_id.id,
            'location_id': stock_loc.id,
            'location_dest_id': worker_loc.id,
            })._action_confirm()._action_assign()._action_done()
        self.state = 'done'


class JewelleryIssueVoucherLine(models.Model):
    _name = 'jewellery.issue.voucher.line'


    voucher_id = fields.Many2one('jewellery.issue.voucher', required=True)
    product_id = fields.Many2one('product.product', required=True)
    qty = fields.Float(required=True)
    gross_weight = fields.Float(string="Gross Weight (g)")
    stone_weight = fields.Float(string="Stone Weight (g)")
    diamond_weight = fields.Float(string="Diamond Weight (g)")
    uom_id = fields.Many2one('uom.uom', string="UoM")
    purity_id = fields.Many2one('gold.purity', string="Purity")


    net_weight = fields.Float(
        string="Net Weight (g)",
        compute="_compute_net_weight",
        store=True
    )

    @api.depends(
        'gross_weight',
        'stone_weight',
        'diamond_weight'
    )
    def _compute_net_weight(self):
        for rec in self:
            rec.net_weight = (
                    rec.gross_weight
                    - rec.stone_weight
                    - rec.diamond_weight
            )