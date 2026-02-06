from odoo import models, fields, api

class DiseaseReportWizard(models.TransientModel):
    _name = 'hr.hospital.disease.report.wizard'
    _description = 'Disease Analysis Report'

    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    disease_ids = fields.Many2many('hr.hospital.disease', string='Specific Diseases')

    def action_print_report(self):
        # Тут зазвичай викликається action для PDF або Excel звіту
        # Поки що просто закриваємо вікно
        return {'type': 'ir.actions.act_window_close'}