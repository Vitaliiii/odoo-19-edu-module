from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _inherit = ['hr.hospital.person']
    _description = 'Hospital Doctor'

    user_id = fields.Many2one(
        comodel_name='res.users',
        string='System User',
    )
    
    specialty_id = fields.Many2one(
        comodel_name='hr.hospital.specialty',
        string='Specialty',
    )
    
    is_intern = fields.Boolean(
        string='Is Intern',
        default=False,
    )
    
    mentor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Mentor Doctor',
        domain="[('is_intern', '=', False)]",
    )
    
    license_number = fields.Char(
        string='License Number',
        required=True,
        copy=False,
    )
    
    license_date = fields.Date(string='License Issue Date')
    
    experience_years = fields.Integer(
        string='Experience (Years)',
        compute='_compute_experience_years',
    )
    
    rating = fields.Float(
        string='Rating',
        default=0.0,
        help="Doctor's rating from 0.00 to 5.00"
    )
    
    education_country_id = fields.Many2one(
        comodel_name='res.country',
        string='Country of Education',
    )

    schedule_ids = fields.One2many(
        comodel_name='hr.hospital.doctor.schedule',
        inverse_name='doctor_id',
        string='Work Schedule',
    )
    
    patient_ids = fields.One2many(
        comodel_name='hr.hospital.patient',
        inverse_name='doctor_id',
        string='Patients',
    )

    _sql_constraints = [
        (
            'unique_license_number',          # 1. Назва
            'UNIQUE(license_number)',         # 2. SQL
            'The license number must be unique!' # 3. Повідомлення
        ),
        (
            'check_rating_range',             
            'CHECK(rating >= 0 AND rating <= 5)', 
            'Rating must be between 0.00 and 5.00!'
        ),
    ]

    @api.depends('license_date')
    def _compute_experience_years(self):
        today = fields.Date.today()
        for rec in self:
            if rec.license_date:
                rec.experience_years = relativedelta(today, rec.license_date).years
            else:
                rec.experience_years = 0

    def _compute_display_name(self):
        for rec in self:
            specialty = rec.specialty_id.name or _('No Specialty')
            rec.display_name = f"{rec.name} ({specialty})"

    @api.constrains('mentor_id', 'is_intern')
    def _check_mentor_validity(self):
        for rec in self:
            if rec.is_intern and rec.mentor_id:
                if rec.mentor_id == rec:
                    raise ValidationError(_("A doctor cannot be their own mentor!"))
                if rec.mentor_id.is_intern:
                    raise ValidationError(_("An intern cannot be appointed as a mentor!"))

    @api.onchange('is_intern')
    def _onchange_is_intern(self):
        if not self.is_intern:
            self.mentor_id = False

    def write(self, vals):
        if 'active' in vals and not vals['active']:
            active_visits = self.env['hr.hospital.visit'].search_count([
                ('doctor_id', 'in', self.ids),
                ('state', '=', 'planned')
            ])
            if active_visits > 0:
                raise ValidationError(_("Cannot archive doctor with active planned visits!"))
        return super().write(vals)