from odoo import models, fields

class HospitalSpecialty(models.Model):
    _name = 'hr.hospital.specialty'
    _description = 'Doctor Specialty'
    
    name = fields.Char(
        string='Specialty Name',
        required=True,
    )
    
    code = fields.Char(
        string='Specialty Code',
        size=10,
        required=True,
        help="Unique code for the specialty (e.g., CARD-01)"
    )
    
    description = fields.Text(string='Description')
    
    active = fields.Boolean(
        string='Active',
        default=True,
        help="If unchecked, this specialty will be hidden from selection."
    )
    
    doctor_ids = fields.One2many(
        comodel_name='hr.hospital.doctor',
        inverse_name='specialty_id',
        string='Doctors',
    )

    _sql_constraints = [
        ('unique_specialty_code', 'UNIQUE(code)', 
         'Specialty code must be unique!')
    ]