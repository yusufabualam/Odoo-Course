from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError
from validate_email_address import validate_email
import re
from dateutil.relativedelta import relativedelta


class Patient(models.Model):
    _name = 'hms.patient'
    _description = 'Patient'
    _rec_name = 'f_name'

    f_name = fields.Char('First Name', required=True)
    l_name = fields.Char('Last Name' , required=True)
    birth_date = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float('CR Ratio')
    blood_type = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'),
    ])
    status = fields.Selection([
        ('undetermined','Undetermined'),
        ('good','Good'),
        ('fair','Fair'),
        ('serious','Serious'),
    ])
    pcr = fields.Boolean('PCR')
    image = fields.Binary()
    address = fields.Text()
    age = fields.Integer(compute='_compute_age')
    department_id = fields.Many2one('hms.department', domain="[('is_opened', '=', True)]")
    doctor_ids = fields.Many2many('hms.doctor', readonly=True, compute='_compute_doctor_ids')
    department_capacity = fields.Integer(related = "department_id.capacity")
    log_ids = fields.One2many('hms.log' , 'patient_id')
    email = fields.Char(required=True, unique=True)

    @api.onchange('department_id')
    def _onchange_department_id(self):
        if self.department_id:
            self.doctor_ids = [(6, 0, [])]
            return {'domain': {'doctor_ids': [('department_ids', '=', self.department_id.id)]}}
        else:
            return {'domain': {'doctor_ids': []}}
    def action_undetermined(self):
        for patient in self:
            patient.write({"status":"undetermined"})
            patient.log_ids.create({
                "patient_id":patient.id,
                "description":"The status is changed to undetermined"
            })
    def action_good(self):
        for patient in self:
            patient.write({"status":"good"})
            patient.log_ids.create({
                "patient_id":patient.id,
                "description":"The status is changed to good"
            })
    def action_fair(self):
        for patient in self:
            patient.write({"status":"fair"})
            patient.log_ids.create({
                "patient_id":patient.id,
                "description":"The status is changed to fair"
            })
    def action_serious(self):
        for patient in self:
            patient.write({"status":"serious"})
            patient.log_ids.create({
                "patient_id":patient.id,
                "description":"The status is changed to serious"
            })

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            if record.email:
                if not re.match(r"[^@]+@[^@]+\.[^@]+", record.email):
                    raise ValidationError("Invalid email address: %s" % record.email)

    @api.constrains('pcr', 'age')
    def _check_pcr_age(self):
        for patient in self:
            if not patient.pcr and patient.age < 30:
                raise ValidationError("You cannot uncheck PCR for patients under the age of 30.")
    @api.depends('birth_date')
    def _compute_age(self):
        for patient in self:
            if patient.birth_date:
                patient.age = relativedelta(fields.Date.today(), patient.birth_date).years
            else:
                patient.age = False

    @api.constrains('pcr', 'cr_ratio')
    def _check_cr_ratio_required(self):
        for patient in self:
            if patient.pcr and not patient.cr_ratio:
                raise ValidationError("CR Ratio is required when PCR is checked.")

    def action_add_log(self):
        action = self.env['ir.actions.actions']._for_xml_id('hms_app.log_wizard_action')
        action['context'] = {
            'default_patient_id': self.id,
        }
        return action

    @api.depends('department_id')
    def _compute_doctor_ids(self):
        for patient in self:
            if patient.department_id:
                doctors = self.env['hms.doctor'].search([('department_id', '=', patient.department_id.id)])
                patient.doctor_ids = [(6, 0, doctors.ids)]
            else:
                patient.doctor_ids = [(5, 0, 0)]