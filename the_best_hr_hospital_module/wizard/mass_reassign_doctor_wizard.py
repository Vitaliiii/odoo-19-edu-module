from odoo import models, fields, api, _

class MassReassignDoctorWizard(models.TransientModel):
    _name = 'hr.hospital.mass.reassign.doctor.wizard'
    _description = 'Mass Reassign Doctor Wizard'

    old_doctor_id = fields.Many2one('hr.hospital.doctor', string='Current Doctor', required=True)
    new_doctor_id = fields.Many2one('hr.hospital.doctor', string='New Doctor', required=True)
    patient_ids = fields.Many2many('hr.hospital.patient', string='Patients to Update')
    reason = fields.Text(string='Reason for Reassignment')

    @api.onchange('old_doctor_id')
    def _onchange_old_doctor_id(self):
        if self.old_doctor_id:
            patients = self.env['hr.hospital.patient'].search([('doctor_id', '=', self.old_doctor_id.id)])
            self.patient_ids = [(6, 0, patients.ids)]

    def action_reassign(self):
        self.ensure_one()
        if self.patient_ids:
            self.patient_ids.write({'doctor_id': self.new_doctor_id.id})
        return {'type': 'ir.actions.act_window_close'}