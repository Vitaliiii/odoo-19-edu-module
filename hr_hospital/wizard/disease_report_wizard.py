from odoo import models, fields, api, _

class DiseaseReportWizard(models.TransientModel):
    _name = 'hr.hospital.disease.report.wizard'
    _description = 'Disease Analysis Report'

    # Додано поле для вибору лікарів
    doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
        string='Doctors',
        help="Leave empty to include all doctors."
    )
    
    disease_ids = fields.Many2many(
        comodel_name='hr.hospital.disease', 
        string='Specific Diseases',
        help="Leave empty to include all diseases."
    )
    
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)

    @api.model
    def default_get(self, fields_list):
        """Автоматично підставляє лікарів, якщо візард викликано з їхньої картки/списку"""
        res = super().default_get(fields_list)
        if self.env.context.get('active_model') == 'hr.hospital.doctor':
            active_ids = self.env.context.get('active_ids')
            if active_ids:
                res['doctor_ids'] = [(6, 0, active_ids)]
        return res

    def action_print_report(self):
        """Формує домен і відкриває список діагнозів"""
        self.ensure_one()
        
        # Базовий домен по датах
        domain = [
            ('date_of_diagnosis', '>=', self.start_date),
            ('date_of_diagnosis', '<=', self.end_date),
        ]
        
        # Додаємо умову по лікарях (шукаємо через візит)
        if self.doctor_ids:
            domain.append(('visit_id.doctor_id', 'in', self.doctor_ids.ids))
            
        # Додаємо умову по хворобах
        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))

        # Повертаємо Action для відкриття моделі Діагнозів
        return {
            'name': _('Disease Report'),
            'type': 'ir.actions.act_window',
            'res_model': 'hr.hospital.diagnosis',
            'view_mode': 'list,form,pivot,graph',
            'domain': domain,
            # Автоматичне групування по хворобах
            'context': {'group_by': ['disease_id']},
            'target': 'current',
        }