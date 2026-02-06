from odoo import models, fields


class HospitalDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Disease'
    
    # --- Налаштування ієрархії (Пункт 4) ---
    # Вказуємо поле, яке є батьківським
    _parent_name = 'parent_id'
    # Вмикаємо оптимізацію зберігання дерева (потребує поля parent_path)
    # Це дозволяє робити швидкий пошук "всіх підкатегорій"
    _parent_store = True
    # Вказуємо поле для відображення в Many2one (назва хвороби)
    _rec_name = 'name'

    name = fields.Char(
        string='Name',
        required=True,
    )
    
    description = fields.Text(string='Description')

    # --- Ієрархічні поля ---
    parent_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Parent Disease',
        index=True,
        ondelete='cascade',
    )
    
    # Це технічне поле потрібне для роботи _parent_store=True
    # Воно зберігає шлях типу "1/5/12/", що дозволяє швидко шукати всіх нащадків
    parent_path = fields.Char(index=True)
    
    child_ids = fields.One2many(
        comodel_name='hr.hospital.disease',
        inverse_name='parent_id',
        string='Sub-diseases',
    )

    # --- Специфічні медичні поля ---
    icd10_code = fields.Char(
        string='ICD-10 Code',
        size=10, # Обмеження довжини на рівні БД
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
    
    # Регіон поширення
    region_ids = fields.Many2many(
        comodel_name='res.country',
        string='Regions',
    )