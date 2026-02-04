from odoo import models, fields


class HospitalDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Disease Type'

    name = fields.Char(required=True)
    description = fields.Text(string='Description')