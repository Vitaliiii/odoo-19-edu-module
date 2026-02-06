from odoo import models, fields


class HospitalContactPerson(models.Model):
    _name = 'hr.hospital.contact.person'
    _inherit = ['hr.hospital.person']
    _description = 'Contact Person'

    description = fields.Text(string='Notes')
    
    # Додаємо поле, щоб було куди застосувати домен
    patient_ids = fields.One2many(
        comodel_name='hr.hospital.patient',
        inverse_name='contact_person_id',
        string='Patients',
        # Тільки алергіки
        domain="[('allergies', '!=', False)]"
    )