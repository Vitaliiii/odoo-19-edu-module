{
    'name': 'Hospital Automation',
    'version': '19.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Manage Doctors and Patients',
    'author': 'Vitaliy',  # Ваше ім’я
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_hospital_menus.xml',
        'views/doctor_views.xml',
        'views/patient_views.xml',
        'views/disease_views.xml',
        'views/visit_views.xml',
        'data/disease_data.xml',
    ],
    'demo': [
        'demo/doctor_demo.xml',
        'demo/patient_demo.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}