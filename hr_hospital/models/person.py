import re
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HospitalPerson(models.AbstractModel):
    _name = 'hr.hospital.person'
    _description = 'Abstract Person'
    _inherit = ['image.mixin']

    last_name = fields.Char(string='Last Name', required=True)
    first_name = fields.Char(string='First Name', required=True)
    middle_name = fields.Char(string='Middle Name')
    
    name = fields.Char(
        string='Full Name',
        compute='_compute_full_name',
        store=True,
        index=True
    )

    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    
    gender = fields.Selection(
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ],
        string='Gender',
        default='male',
    )
    date_of_birth = fields.Date(string='Date of Birth')
    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        store=True,
    )

    citizenship_country_id = fields.Many2one(
        comodel_name='res.country',
        string='Citizenship'
    )
    language_id = fields.Many2one(
        comodel_name='res.lang',
        string='Preferred Language'
    )

    @api.depends('last_name', 'first_name', 'middle_name')
    def _compute_full_name(self):
        """Збирає ПІБ в один рядок"""
        for rec in self:
            name_parts = [
                part for part in [rec.last_name, rec.first_name, rec.middle_name] 
                if part
            ]
            rec.name = " ".join(name_parts)

    @api.depends('date_of_birth')
    def _compute_age(self):
        """Обчислює вік на основі поточної дати"""
        today = fields.Date.today()
        for rec in self:
            if rec.date_of_birth:
                rec.age = relativedelta(today, rec.date_of_birth).years
            else:
                rec.age = 0

    @api.constrains('email')
    def _check_email_validity(self):
        """Перевірка формату Email через Regex"""
        for rec in self:
            if rec.email:
                pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
                if not re.match(pattern, rec.email):
                    raise ValidationError(_("Invalid email format for %s") % rec.name)

    @api.constrains('phone')
    def _check_phone_validity(self):
        """Перевірка формату телефону (мінімум 10 цифр)"""
        for rec in self:
            if rec.phone:
                digits_only = re.sub