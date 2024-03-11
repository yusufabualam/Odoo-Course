from odoo import fields, models, api


class Log(models.Model):
    _name = 'hms.log'
    _description = 'Log'
    _rec_name = 'created_by'

    created_by = fields.Many2one("res.users")
    date = fields.Date(default=fields.Date.today, readonly=True)
    description = fields.Text()
    patient_id = fields.Many2one('hms.patient', readonly=True, required=True)

    @api.model
    def create(self, vals):
        vals["created_by"] = self.env.user.id
        return super(Log, self).create(vals)
