from odoo import fields, models


class Doctor(models.Model):
    _name = 'hms.doctor'
    _description = 'Doctor'
    _rec_name = 'f_name'

    f_name = fields.Char("First Name")
    l_name = fields.Char('Last Name')
    image = fields.Binary()
    department_id = fields.Many2one('hms.department')
    patient_ids = fields.Many2many('hms.patient')

