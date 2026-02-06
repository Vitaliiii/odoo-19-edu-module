from odoo import models, fields


class HospitalDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Disease'
    _parent_name = 'parent_id'
    _parent_store = True
    _rec_name = 'name'

    name = fields.Char(
        string='Name',
        required=True,
    )
    
    description = fields.Text(string='Description')

    parent_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Parent Disease',
        index=True,
        ondelete='cascade',
    )
    
    parent_path = fields.Char(index=True)
    
    child_ids = fields.One2many(
        comodel_name='hr.hospital.disease',
        inverse_name='parent_id',
        string='Sub-diseases',
    )

    icd10_code = fields.Char(
        string='ICD-10 Code',
        size=10,
    )
    
    severity = fields.Selection(
        selection=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ],
        string='Severity',
    )
    
    is_infectious = fields.Boolean(string='Infectious')
    
    symptoms = fields.Text(string='Symptoms')
    
    region_ids = fields.Many2many(
        comodel_name='res.country',
        string='Regions',
    )