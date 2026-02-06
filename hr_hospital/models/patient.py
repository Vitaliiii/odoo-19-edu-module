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

    passport_data = fields.Char(
        string='Passport Details',
        size=10,
    )

    contact_person_id = fields.Many2one(
        comodel_name='hr.hospital.contact.person',
        string='Emergency Contact',
    )

    blood_type = fields.Selection(
        selection=[
            ('o_plus', 'O(I) Rh+'), ('o_minus', 'O(I) Rh-'),
            ('a_plus', 'A(II) Rh+'), ('a_minus', 'A(II) Rh-'),
            ('b_plus', 'B(III) Rh+'), ('b_minus', 'B(III) Rh-'),
            ('ab_plus', 'AB(IV) Rh+'), ('ab_minus', 'AB(IV) Rh-'),
        ],
        string='Blood Group',
    )

    allergies = fields.Text(string='Allergies')

    insurance_partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Insurance Company',
        domain="[('is_company', '=', True)]",
    )

    insurance_policy_number = fields.Char(string='Policy Number')

    doctor_history_ids = fields.One2many(
        comodel_name='hr.hospital.patient.doctor.history',
        inverse_name='patient_id',
        string='Physician History',
        readonly=True,
    )

    @api.constrains('date_of_birth')
    def _check_patient_age(self):
        """Перевірка, що вік пацієнта більше 0 (дата народження не в майбутньому)"""
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_("Patient's date of birth cannot be in the future!"))

    @api.onchange('citizenship_country_id')
    def _onchange_citizenship_suggest_lang(self):
        """Пропонуємо мову на основі країни громадянства"""
        if self.citizenship_country_id:
            lang = self.env['res.lang'].search([
                ('code', 'ilike', self.citizenship_country_id.code)
            ], limit=1)
            if lang:
                self.language_id = lang

    def write(self, vals):
        """
        При зміні персонального лікаря (doctor_id) 
        автоматично створюємо запис в моделі історії.
        """
        if 'doctor_id' in vals:
            for rec in self:
                if rec.doctor_id.id != vals.get('doctor_id'):
                    self.env['hr.hospital.patient.doctor.history'].create({
                        'patient_id': rec.id,
                        'doctor_id': vals.get('doctor_id'),
                        'appointment_date': fields.Date.context_today(self),
                    })
        return super(HospitalPatient, self).write(vals)