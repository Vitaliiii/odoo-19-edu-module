from odoo import models, fields, api
from datetime import timedelta

class DoctorScheduleWizard(models.TransientModel):
    _name = 'hr.hospital.doctor.schedule.wizard'
    _description = 'Generate Doctor Schedule'

    doctor_id = fields.Many2one('hr.hospital.doctor', string='Doctor', required=True)
    week_start_date = fields.Date(string='Start From', default=fields.Date.today, required=True)
    weeks_count = fields.Integer(string='Number of Weeks', default=1)
    
    schedule_type = fields.Selection([
        ('work', 'Working Days'),
        ('conference', 'Conference Week')
    ], default='work', required=True)

    time_start = fields.Float(string='Start Time', default=9.0)
    time_end = fields.Float(string='End Time', default=18.0)

    def action_generate_schedule(self):
        self.ensure_one()
        schedule_obj = self.env['hr.hospital.doctor.schedule']
        
        for week in range(self.weeks_count):
            for day in range(5):
                current_date = self.week_start_date + timedelta(weeks=week, days=day)
                schedule_obj.create({
                    'doctor_id': self.doctor_id.id,
                    'schedule_date': current_date,
                    'day_of_week': str(day),
                    'time_start': self.time_start,
                    'time_end': self.time_end,
                    'activity_type': self.schedule_type,
                })
        return {'type': 'ir.actions.act_window_close'}