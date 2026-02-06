# -*- coding: utf-8 -*-
{
    'name': "Hospital Management",
    'summary': "Comprehensive hospital and clinic management system",
    'description': """
        Module for managing hospital operations:
        - Doctor and Patient profiles
        - Medical Diagnoses and Disease hierarchy
        - Visit scheduling and history tracking
        - Specialized wizards for data management
    """,
    'author': "Vitalii",
    'website': '',
    'category': 'Customizations/Medical',
    'version': '19.0.1.0.0',

    # Базові модулі Odoo, необхідні для роботи
    'depends': ['base'],

    # Файли, які завантажуються завжди
    'data': [
        'security/ir.model.access.csv',
        'views/wizard_views.xml',
        'views/specialty_views.xml', 
        'views/disease_views.xml',
        'views/doctor_views.xml',
        'views/patient_views.xml',
        'views/visit_views.xml',
        'views/hr_hospital_menus.xml',
    ],

    # Демо-дані (завантажуються тільки якщо ввімкнено "Load demo data" при створенні БД)
    'demo': [
        'data/demo_data.xml',
    ],

    'installable': True,
    'application': True,  # Модуль буде відображатися в основному списку Apps
    'auto_install': False,
    'license': 'LGPL-3',
}