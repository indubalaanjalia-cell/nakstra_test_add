from odoo import models, fields

class JewelleryLabTest(models.Model):
    _name = 'jewellery.lab.test'
    _description = 'Jewellery Lab Purity Test'

    job_work_id = fields.Many2one(
        'jewellery.job.work',
        string='Job Work',
        ondelete='cascade',
        required=True
    )

    lab_partner_id = fields.Many2one(
        'res.partner',
        string='Lab'
    )

    sample_ref = fields.Char(string='Sample Reference')

    metal_type = fields.Selection([
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('alloy', 'Alloy')
    ], string='Metal Type')

    issued_weight = fields.Float(string='Issued Sample Weight')
    test_date = fields.Date(string='Test Date')

    report_no = fields.Char(string='Lab Report No')

    remarks = fields.Text(string='Remarks')

    state = fields.Selection([
        ('sent', 'Sent to Lab'),
        ('received', 'Result Received')
    ], default='sent', string='Status')
    expected_purity_id = fields.Many2one('gold.purity', string="Expected Purity")
    tested_purity_id = fields.Many2one('gold.purity', string="Tested Purity")
