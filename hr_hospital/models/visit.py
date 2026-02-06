from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError


class HospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Patient Visit'
    _order = 'visit_date_planned desc'

    # --- Відображення імені (Виправлення Virtual ID) ---

    def _compute_display_name(self):
        """
        Метод формує зрозумілу назву для запису.
        Замість технічного NewId_0x... користувач побачить 'Пацієнт (Дата)'.
        """
        for rec in self:
            # Форматуємо дату, якщо вона заповнена
            if rec.visit_date_planned:
                # Наприклад: 2026-02-06 14:30
                date_str = rec.visit_date_planned.strftime('%Y-%m-%d %H:%M')
            else:
                date_str = _("New Date")
            
            # Беремо ім'я пацієнта або пишемо "Новий пацієнт"
            patient_name = rec.patient_id.name or _("New Patient")
            
            rec.display_name = f"{patient_name} ({date_str})"

    # --- Статус та дати (Пункт 2.3) ---
    state = fields.Selection(
        selection=[
            ('planned', 'Planned'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
            ('missed', 'No Show'),
        ],
        string='Status',
        default='planned',
        required=True,
    )
    
    visit_date_planned = fields.Datetime(
        string='Planned Date and Time',
        required=True,
        index=True,
        default=fields.Datetime.now,
    )
    
    # Фактична дата
    visit_date_actual = fields.Datetime(
        string='Actual Visit Date',
        readonly=True,
    )

    # --- Учасники ---
    # Вимога 8.1: Домен - лікар має мати ліцензію
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor',
        required=True,
        domain="[('license_number', '!=', False)]"
    )
    
    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Patient',
        required=True,
    )

    # --- Деталі ---
    visit_type = fields.Selection(
        selection=[
            ('first', 'Initial'),
            ('repeat', 'Follow-up'),
            ('preventive', 'Check-up'),
            ('urgent', 'Emergency'),
        ],
        string='Visit Type',
    )
    
    diagnosis_ids = fields.One2many(
        comodel_name='hr.hospital.diagnosis',
        inverse_name='visit_id',
        string='Diagnoses',
    )
    
    recommendations = fields.Html(string='Recommendations')

    # --- Фінанси ---
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
    )
    amount = fields.Monetary(
        string='Visit Cost',
        currency_field='currency_id',
    )

    # --- Обмеження (Пункт 5.2 та 5.3) ---

    @api.constrains('visit_date_planned', 'doctor_id', 'patient_id')
    def _check_unique_visit_per_day(self):
        """Заборона запису одного пацієнта до одного лікаря більше одного разу на день"""
        for rec in self:
            if not rec.visit_date_planned:
                continue
            visit_date = rec.visit_date_planned.date()
            
            # Шукаємо дублікати на ту саму дату
            domain = [
                ('id', '!=', rec.id),
                ('doctor_id', '=', rec.doctor_id.id),
                ('patient_id', '=', rec.patient_id.id),
            ]
            existing_visits = self.search(domain)
            
            for exist in existing_visits:
                if exist.visit_date_planned.date() == visit_date:
                    raise ValidationError(_("This patient already has a visit scheduled for this doctor on %s") % visit_date)

    @api.constrains('visit_date_actual', 'visit_date_planned')
    def _check_dates_order(self):
        """Фактична дата не може бути раніше запланованої"""
        for rec in self:
            if rec.visit_date_actual and rec.visit_date_actual < rec.visit_date_planned:
                raise ValidationError(_("Actual visit date cannot be earlier than the planned date."))

    def unlink(self):
        """Заборона видалення візитів з діагнозами (Пункт 5.3)"""
        for rec in self:
            if rec.diagnosis_ids:
                raise UserError(_("You cannot delete a visit that already has diagnoses recorded."))
        return super().unlink()

    # --- Методи Onchange (Пункт 6.3) ---

    @api.onchange('patient_id')
    def _onchange_patient_id(self):
        """Показувати попередження про алергії"""
        if self.patient_id and self.patient_id.allergies:
            return {
                'warning': {
                    'title': _("Allergy Warning!"),
                    'message': _("The patient has the following allergies: %s") % self.patient_id.allergies,
                }
            }