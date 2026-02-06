from datetime import timedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class HospitalDiagnosis(models.Model):
    _name = 'hr.hospital.diagnosis'
    _description = 'Medical Diagnosis'

    # --- Зв'язки ---
    
    # Вимога 8.1: Домен - показувати тільки завершені візити
    # Вимога 3.1: ondelete='cascade'
    visit_id = fields.Many2one(
        comodel_name='hr.hospital.visit',
        string='Visit',
        required=True,
        ondelete='cascade',
        domain="[('state', '=', 'done')]"
    )

    # Вимога 8.1: Домен - показувати тільки заразні хвороби з високим/критичним ступенем
    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Disease',
        required=True,
        domain="[('is_infectious', '=', True), ('severity', 'in', ['high', 'critical'])]"
    )

    # --- Опис ---
    description = fields.Text(string='Description')
    treatment_notes = fields.Html(string='Treatment')
    
    severity = fields.Selection(
        selection=[
            ('mild', 'Mild'),
            ('moderate', 'Moderate'),
            ('severe', 'Severe'),
            ('critical', 'Critical'),
        ],
        string='Severity',
    )

    # --- Блок затвердження (Approval) ---
    is_approved = fields.Boolean(
        string='Approved',
        default=False,
    )
    approved_by_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Approved By',
        readonly=True,
    )
    approved_date = fields.Datetime(
        string='Approval Date',
        readonly=True,
    )

    # --- Методи Бізнес-логіки (Пункт 6) ---

    def action_approve(self):
        """
        Затверджує діагноз. Перевіряє, чи користувач пов'язаний з лікарем.
        """
        for rec in self:
            if rec.is_approved:
                raise UserError(_("Diagnosis is already approved."))

            # Шукаємо лікаря, який прив'язаний до поточного користувача
            current_doctor = self.env['hr.hospital.doctor'].search(
                [('user_id', '=', self.env.user.id)], limit=1
            )

            if not current_doctor:
                raise UserError(_("Your user is not linked to any Doctor profile."))

            # Оновлюємо поля
            rec.write({
                'is_approved': True,
                'approved_by_id': current_doctor.id,
                'approved_date': fields.Datetime.now()
            })

    # --- Динамічні домени (Пункт 8.2) ---

    @api.onchange('visit_id')
    def _onchange_visit_domain(self):
        """
        Динамічно обмежує вибір візитів:
        тільки завершені візити за останні 30 днів.
        """
        date_threshold = fields.Datetime.now() - timedelta(days=30)
        
        return {
            'domain': {
                'visit_id': [
                    ('state', '=', 'done'),
                    ('visit_date_planned', '>=', date_threshold)
                ]
            }
        }