from odoo import models, fields


class HospitalDoctorSchedule(models.Model):
    _name = 'hr.hospital.doctor.schedule'
    _description = 'Doctor Schedule'
    _rec_name = 'doctor_id'  # Для зручного відображення в хлібних крихтах

    # Вимога 8.1: При створенні розкладу показувати тільки лікарів з заповненою спеціальністю
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor',
        required=True,
        domain="[('specialty_id', '!=', False)]"
    )
    
    # День тижня (0 = Понеділок, 6 = Неділя)
    # Використовується для повторюваних графіків
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
    
    # Конкретна дата (має пріоритет над днем тижня або використовується для винятків)
    schedule_date = fields.Date(string='Specific Date')
    
    # Час у форматі Float (наприклад, 14.5 = 14:30)
    # У XML views до цих полів варто додати widget="float_time"
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