from odoo import models, fields, api


class JewelleryJobWork(models.Model):
    _name = 'jewellery.job.work'
    _description = 'Jewellery Job Work Voucher'


    name = fields.Char(string='Job Work Number', copy=False, readonly=True, default='New')
    job_worker_id = fields.Many2one('res.partner', domain=[('is_job_worker','=',True)], required=True)
    job_type = fields.Selection([
    ('gold_only', 'Gold Only'),
    ('gold_alloy', 'Gold + Alloy')
    ], required=True)
    mo_id = fields.Many2one('mrp.production')
    issue_voucher_ids = fields.One2many(
        'jewellery.issue.voucher', 'job_work_id'
    )
    receive_voucher_ids = fields.One2many(
        'jewellery.receive.voucher', 'job_work_id'
    )
    making_charge_bill_id = fields.Many2one(
        'account.move', readonly=True
    )
    making_charge_amount = fields.Monetary(string='Making Charge', currency_field='currency_id')
    making_charge_bill_ids = fields.One2many(
        'account.move', 'job_work_id', string='Making Charge Bills'
    )
    currency_id = fields.Many2one('res.currency', string='Currency', default=lambda self: self.env.company.currency_id)

    state = fields.Selection([
        ('draft','Draft'),('issued','Issued'),('received','Received'),('done','Done')
    ], default='draft')


    show_issue_btn = fields.Boolean(compute='_compute_buttons')
    show_receive_btn = fields.Boolean(compute='_compute_buttons')
    show_bill_btn = fields.Boolean(compute='_compute_buttons')
    lab_test_ids = fields.One2many(
        'jewellery.lab.test',
        'job_work_id',
        string='Lab Details'
    )
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('jewellery.job.work') or 'New'
        return super().create(vals)

    @api.depends('state')
    def _compute_buttons(self):
        for rec in self:
            rec.show_issue_btn = rec.state == 'draft'
            rec.show_receive_btn = rec.state == 'issued'
            rec.show_bill_btn = rec.state == 'received'

    def action_create_issue_voucher(self):
        self.ensure_one()
        voucher = self.env['jewellery.issue.voucher'].create({
            'job_work_id': self.id,
            'job_worker_id': self.job_worker_id.id,
        })
        if voucher:
            self.state ='issued'

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'jewellery.issue.voucher',
            'view_mode': 'form',
            'res_id': voucher.id,
        }
    def action_create_receive_voucher(self):
        self.ensure_one()
        voucher = self.env['jewellery.receive.voucher'].create({
            'job_work_id': self.id,
            'job_worker_id': self.job_worker_id.id,

        })
        if voucher:
            self.state = 'received'
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'jewellery.receive.voucher',
            'view_mode': 'form',
            'res_id': voucher.id,
        }

    def action_create_making_charge_bill(self):
        self.ensure_one()
        if not self.making_charge_amount or not self.job_worker_id:
            return False

        # Create the vendor bill
        bill = self.env['account.move'].create({
            'move_type': 'in_invoice',
            'partner_id': self.job_worker_id.id,
            'invoice_line_ids': [(0, 0, {
                'name': f'Making Charge - {self.name}',
                'quantity': 1,
                'price_unit': self.making_charge_amount,
            })],
            'job_work_id': self.id,
        })
        if bill:
            self.making_charge_bill_id =bill.id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': bill.id,
            'target': 'new',
        }

    def action_view_making_charge_bills(self):
        """Smart button to show all making charge bills"""
        self.ensure_one()
        return {
            'name': 'Making Charge Bills',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'domain': [('job_work_id', '=', self.id)],
            'view_mode': 'tree,form',
            'target': 'current',
        }