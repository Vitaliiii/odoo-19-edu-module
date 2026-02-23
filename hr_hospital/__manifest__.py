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
    'category': 'Customizations/Medical',
    'version': '19.0.1.0.2',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        
        'reports/doctor_report.xml',
        
        'wizard/wizard_views.xml',
                
        'views/specialty_views.xml', 
        'views/disease_views.xml',
        
        'views/doctor_views.xml',
        'views/patient_views.xml',

        'views/visit_views.xml',
        'views/diagnosis_views.xml',

        'views/hr_hospital_menus.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'images': ['static/description/icon.png'],
}