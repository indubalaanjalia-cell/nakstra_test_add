from odoo import models, fields, api


class PurchaseRequisition(models.Model):
    _inherit = 'material.purchase.requisition'

    job_work_id = fields.Many2one(
        'jewellery.job.work',
        string='Job Work',
        ondelete='cascade',
        required=True
    )

    def action_create_picking_and_po(self):
        res = super().action_create_picking_and_po()
        for line in self.requisition_lines:
            if line.request_action == "work order":
                for vendor in line.vendor_ids:
                    work_vals = {

                        "job_worker_id": vendor.id,
                        "job_work_line_ids": [
                            (
                                0,
                                0,
                                {
                                    "product_id": line.product_id.id,
                                    "quantity": line.quantity,
                                    "no_of_pieces": line.source_location_id.id,
                                    "gram_range_id": line.gram_range_id.id,
                                    "purity_id": line.purity_id.id,
                                    "unit_of_measure": line.product_id.uom_id.id,
                                },
                            )
                        ],
                    }

                    work = self.env["work.order"].create(work_vals)
                    line.write({"job_work_id": work.id})

class MaterialPurchaseRequisitionLine(models.Model):
    _inherit = "material.purchase.requisition.line"

    purity_id = fields.Many2one('gold.purity', string="Purity")
