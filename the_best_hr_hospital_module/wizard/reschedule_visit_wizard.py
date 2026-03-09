from odoo import models, fields, api

class RescheduleVisitWizard(models.TransientModel):
    _name = 'hr.hospital.reschedule.visit.wizard'
    _description = 'Reschedule Visit'

    visit_id = fields.Many2one('hr.hospital.visit', string='Visit', readonly=True)
    new_date = fields.Datetime(string='New Date', required=True)
    reason = fields.Char(string='Reason')

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if self.env.context.get('active_model') == 'hr.hospital.visit':
            res['visit_id'] = self.env.context.get('active_id')
        return res

    def action_reschedule(self):
        self.ensure_one()
        self.visit_id.write({
            'visit_date_planned': self.new_date,
            'recommendations': (self.visit_id.recommendations or '') + f"\nRescheduled: {self.reason}"
        })