from odoo import models, fields


class HospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _description = 'Hospital Patient'

    name = fields.Char(string='Patient Name', required=True)
    date_of_birth = fields.Date(string='Date of Birth')
    gender = fields.Selection(
        selection=[('male', 'Male'), ('female', 'Female')],
        string='Gender',
    )
    
    # Сімейний лікар / Лікар, що спостерігає пацієнта
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Personal Doctor',
    )
    
    disease_ids = fields.Many2many(
        comodel_name='hr.hospital.disease',
        string='Diseases',
    )