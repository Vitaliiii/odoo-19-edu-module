from odoo import models, fields


class HospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _description = 'Hospital Doctor'

    name = fields.Char(string='Doctor Name', required=True)
    specialization = fields.Char(string='Specialization')
    
    # "Лікар, що спостерігає" (якщо мається на увазі ментор для лікаря)
    mentor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Supervisor/Mentor Doctor',
    )
    
    patient_ids = fields.One2many(
        comodel_name='hr.hospital.patient',
        inverse_name='doctor_id',
        string='Patients',
    ) 