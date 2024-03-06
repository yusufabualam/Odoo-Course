from odoo import fields, models


class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient'
    _rec_name = 'f_name'

    f_name = fields.Char('First Name')
    l_name = fields.Char('Last Name')
    birth_date = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float('CR Ratio')
    blood_type = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'),
    ])
    pcr = fields.Boolean('PCR')
    image = fields.Binary()
    address = fields.Text()
    age = fields.Integer()
    status = fields.Selection([
        ('undetermined','Undetermined'),
        ('good','Good'),
        ('fair','Fair'),
        ('serious','Serious'),
    ])
    department_id = fields.Many2one('hms.department')
    doctor_id = fields.Many2one('hms.doctor')
    department_capacity = fields.Integer(related = "department_id.capacity")
