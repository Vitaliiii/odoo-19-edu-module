from odoo import models, fields, api

class PatientCardExportWizard(models.TransientModel):
    _name = 'hr.hospital.patient.card.export.wizard'
    _description = 'Export Patient Card'

    patient_id = fields.Many2one('hr.hospital.patient', string='Patient', required=True)
    include_history = fields.Boolean(string='Include Doctor History', default=True)
    include_diagnoses = fields.Boolean(string='Include Full Diagnoses', default=True)

    def action_export(self):
        return {'type': 'ir.actions.act_window_close'}