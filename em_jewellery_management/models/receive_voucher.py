from odoo import models, fields, api


class JewelleryReceiveVoucher(models.Model):
    _name = 'jewellery.receive.voucher'
    _description = 'Receive Voucher'

    name = fields.Char(string='Receive Voucher Number', copy=False, readonly=True, default='New')
    job_work_id = fields.Many2one('jewellery.job.work', required=True)
    job_worker_id = fields.Many2one('res.partner', required=True)

    wastage_weight = fields.Float()
    line_ids = fields.One2many('jewellery.receive.voucher.line', 'voucher_id')
    state = fields.Selection([('draft','Draft'),('done','Done')], default='draft')
    active_package_line_ids = fields.One2many(
        'jewellery.receive.voucher.package.line','voucher_id',string='Package Products')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('jewellery.receive.voucher') or 'New'
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
                'location_id': worker_loc.id,
                'location_dest_id': stock_loc.id,
                })._action_confirm()._action_assign()._action_done()
        self.state = 'done'

class JewelleryReceiveVoucherLine(models.Model):
    _name = 'jewellery.receive.voucher.line'


    voucher_id = fields.Many2one('jewellery.receive.voucher', required=True)
    product_id = fields.Many2one('product.template', required=True)
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

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._sync_pack_products()
        return records

    def write(self, vals):
        res = super().write(vals)
        if 'product_id' in vals or 'qty' in vals:
            self._sync_pack_products()
        return res

    def _sync_pack_products(self):
        for line in self:
            line.voucher_id.active_package_line_ids.unlink()
            tmpl = line.product_id
            for pack in tmpl.pack_products_ids:
                self.env['jewellery.receive.voucher.package.line'].create({
                    'product_id': pack.product_id.id,
                    'qty': pack.quantity * line.qty,
                    'uom_id': pack.product_id.uom_id.id,
                    'voucher_id':line.voucher_id.id,
                })

    def unlink(self):
        parents = self.mapped('voucher_id')
        res = super().unlink()

        # force refresh of package tab
        parents.write({'active_package_line_ids': [(5, 0, 0)]})

        return res


class JewelleryReceiveVoucherPackageLine(models.Model):
    _name = 'jewellery.receive.voucher.package.line'
    _description = 'Receive Voucher Package Product'

    voucher_id = fields.Many2one(
        'jewellery.receive.voucher',
        ondelete='cascade',
        required=True
    )
    product_id = fields.Many2one('product.product', required=True)
    qty = fields.Float()
    uom_id = fields.Many2one('uom.uom')