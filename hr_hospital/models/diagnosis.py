from datetime import timedelta
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class HospitalDiagnosis(models.Model):
    _name = 'hr.hospital.diagnosis'
    _description = 'Medical Diagnosis'

    date_of_diagnosis = fields.Date(
        string='Date of Diagnosis', 
        default=fields.Date.context_today
    )
    visit_id = fields.Many2one(
        comodel_name='hr.hospital.visit',
        string='Visit',
        required=True,
        ondelete='cascade',
        domain="[('state', '=', 'done')]"
    )
    
    patient_id = fields.Many2one(
        related='visit_id.patient_id',
        string='Patient',
        store=True,
        readonly=True
    )

    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Disease',
        required=True,
        domain="[('is_infectious', '=', True), ('severity', 'in', ['high', 'critical'])]"
    )

    disease_type_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        related='disease_id.parent_id',
        string='Disease Type',
        store=True,
    )

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

    is_approved = fields.Boolean(string='Approved', default=False)
    approved_by_id = fields.Many2one('hr.hospital.doctor', string='Approved By', readonly=True)
    approved_date = fields.Datetime(string='Approval Date', readonly=True)

    def action_approve(self):
        current_doctor = self.env['hr.hospital.doctor'].search(
            [('user_id', '=', self.env.user.id)], limit=1
        )
        if not current_doctor:
            raise UserError(_("Your user is not linked to any Doctor profile."))

        for rec in self:
            if rec.is_approved:
                raise UserError(_("Diagnosis is already approved."))
            
            rec.write({
                'is_approved': True,
                'approved_by_id': current_doctor.id,
                'approved_date': fields.Datetime.now()
            })

    @api.onchange('visit_id')
    def _onchange_visit_domain(self):
        date_threshold = fields.Datetime.now() - timedelta(days=30)
        return {
            'domain': {
                'visit_id': [
                    ('state', '=', 'done'),
                    ('visit_date_planned', '>=', date_threshold)
                ]
            }
        }
        
    @api.constrains('date_of_diagnosis', 'visit_id')
    def _check_diagnosis_date(self):
        for rec in self:
            if rec.visit_id and rec.date_of_diagnosis:
                if rec.date_of_diagnosis < rec.visit_id.visit_date_planned.date():
                    raise ValidationError(_("The diagnosis date cannot be earlier than the visit date!"))