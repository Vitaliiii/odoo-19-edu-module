from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class HospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _inherit = ['hr.hospital.person']
    _description = 'Hospital Patient'

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Personal Doctor',
        help="Main physician responsible for this patient"
    )

    passport_data = fields.Char(string='Passport Details', size=10)
    contact_person_id = fields.Many2one('hr.hospital.contact.person', string='Emergency Contact')
    
    blood_type = fields.Selection([
        ('o_plus', 'O(I) Rh+'), ('o_minus', 'O(I) Rh-'),
        ('a_plus', 'A(II) Rh+'), ('a_minus', 'A(II) Rh-'),
        ('b_plus', 'B(III) Rh+'), ('b_minus', 'B(III) Rh-'),
        ('ab_plus', 'AB(IV) Rh+'), ('ab_minus', 'AB(IV) Rh-'),
    ], string='Blood Group')

    allergies = fields.Text(string='Allergies')

    insurance_partner_id = fields.Many2one('res.partner', string='Insurance Company', domain="[('is_company', '=', True)]")
    insurance_policy_number = fields.Char(string='Policy Number')

    doctor_history_ids = fields.One2many(
        'hr.hospital.patient.doctor.history', 'patient_id', string='Physician History', readonly=True
    )
    
    # Зв'язок для історії візитів
    visit_ids = fields.One2many('hr.hospital.visit', 'patient_id', string='Visits')
    visit_count = fields.Integer(compute='_compute_visit_count', string='Visit Count')
    
    # Зв'язок для історії діагнозів
    diagnosis_ids = fields.One2many('hr.hospital.diagnosis', 'patient_id', string='Diagnoses')

    def _compute_visit_count(self):
        for rec in self:
            rec.visit_count = len(rec.visit_ids)

    def action_view_visits(self):
        """Smart button: Перехід до списку візитів"""
        return {
            'name': _('Visits'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
        }

    def action_create_visit(self):
        """Кнопка: Швидкий запис до лікаря"""
        return {
            'name': _('Create Visit'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'new',  # Відкрити у модальному вікні
            'context': {
                'default_patient_id': self.id,
                'default_doctor_id': self.doctor_id.id,
            }
        }

    @api.constrains('date_of_birth')
    def _check_patient_age(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_("Patient's date of birth cannot be in the future!"))

    @api.onchange('citizenship_country_id')
    def _onchange_citizenship_suggest_lang(self):
        if self.citizenship_country_id:
            lang = self.env['res.lang'].search([('code', 'ilike', self.citizenship_country_id.code)], limit=1)
            if lang:
                self.language_id = lang

    def write(self, vals):
        if 'doctor_id' in vals:
            history_vals_list = []
            for rec in self:
                if rec.doctor_id.id != vals.get('doctor_id'):
                    history_vals_list.append({
                        'patient_id': rec.id,
                        'doctor_id': vals.get('doctor_id'),
                        'appointment_date': fields.Date.context_today(self),
                    })
            if history_vals_list:
                self.env['hr.hospital.patient.doctor.history'].create(history_vals_list)
                
        return super(HospitalPatient, self).write(vals)