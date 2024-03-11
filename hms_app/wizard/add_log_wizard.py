from odoo import fields, models


class AddLog(models.TransientModel):
    _name = 'log.wizard'
    _description = 'Add Log Wizard'

    patient_id = fields.Many2one('hms.patient')
    log_id = fields.Many2one('hms.log', required=1)

    def action_add_log(self):
        self.ensure_one()
        self.patient_id.write({
            'log_ids': [(4, self.log_id.id)]
        })