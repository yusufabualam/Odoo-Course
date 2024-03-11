from odoo import fields, models, api, exceptions
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('hms.patient')

    @api.constrains('vat')
    def _check_tax_id(self):
        for partner in self:
            if not partner.vat:
                raise ValidationError('Tax ID is required for CRM Customers.')

    @api.constrains('email')
    def _check_unique_email(self):
        for partner in self:
            if partner.email and self.env['hms.patient'].search_count([('email', '=', partner.email)]) > 0:
                raise ValidationError('This email address is already linked to a patient.')
