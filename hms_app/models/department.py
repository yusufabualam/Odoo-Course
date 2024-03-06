from odoo import fields, models


class Department(models.Model):
    _name = 'hms.department'
    _description = 'Department'

    name = fields.Char()
    capacity = fields.Integer()
    is_opened = fields.Boolean()
    patient_ids = fields.One2many('hms.patient', "department_id")
