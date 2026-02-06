from odoo import models, fields, api


class HospitalPatientDoctorHistory(models.Model):
    _name = 'hr.hospital.patient.doctor.history'
    _description = 'Patient Doctor History'

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Patient',
        required=True,
        ondelete='cascade',
    )
    
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor',
        required=True,
        ondelete='cascade',
    )
    
    appointment_date = fields.Date(
        string='Appointment Date',
        required=True,
        default=fields.Date.context_today,
    )
    
    change_date = fields.Date(string='Change Date')
    
    change_reason = fields.Text(string='Reason for Change')
    
    active = fields.Boolean(
        string='Active',
        default=True,
    )

    # --- ВИПРАВЛЕНО: Використовуємо model_create_multi (Пункт 6.4) ---
    
    @api.model_create_multi
    def create(self, vals_list):
        """
        Метод create в Odoo 17+ отримує список словників (vals_list).
        Проходимо циклом по кожному словнику в списку.
        """
        for vals in vals_list:
            patient_id = vals.get('patient_id')
            if patient_id:
                # Шукаємо всі попередні АКТИВНІ записи для цього пацієнта
                old_records = self.search([
                    ('patient_id', '=', patient_id),
                    ('active', '=', True)
                ])
                
                # Якщо знайшли — архівуємо їх (ставимо active=False)
                if old_records:
                    old_records.write({
                        'active': False,
                        'change_date': fields.Date.context_today(self),
                    })
        
        # Викликаємо батьківський метод, передаючи весь список
        return super().create(vals_list)