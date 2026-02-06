from odoo import models, fields


class HospitalDoctorSchedule(models.Model):
    _name = 'hr.hospital.doctor.schedule'
    _description = 'Doctor Schedule'
    _rec_name = 'doctor_id'

    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor',
        required=True,
        domain="[('specialty_id', '!=', False)]"
    )
    
    day_of_week = fields.Selection(
        selection=[
            ('0', 'Monday'),
            ('1', 'Tuesday'),
            ('2', 'Wednesday'),
            ('3', 'Thursday'),
            ('4', 'Friday'),
            ('5', 'Saturday'),
            ('6', 'Sunday'),
        ],
        string='Day of Week',
    )
    
    schedule_date = fields.Date(string='Specific Date')
    
    time_start = fields.Float(
        string='Start Time',
        required=True,
        default=9.0,
    )
    time_end = fields.Float(
        string='End Time',
        required=True,
        default=18.0,
    )
    
    activity_type = fields.Selection(
        selection=[
            ('work', 'Work Day'),
            ('vacation', 'Vacation'),
            ('sick', 'Sick Leave'),
            ('conference', 'Conference'),
        ],
        string='Activity Type',
        default='work',
        required=True,
    )