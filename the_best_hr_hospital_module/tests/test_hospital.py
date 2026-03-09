from datetime import date, timedelta
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestHospitalModels(TransactionCase):

    def setUp(self):
        """Цей метод запускається перед кожним тестом. Тут ми створюємо базові дані."""
        super(TestHospitalModels, self).setUp()
        
        self.doctor = self.env['hr.hospital.doctor'].create({
            'last_name': 'Dr. House',
            'first_name': 'Gregory',
            'license_number': 'LIC12345678',
            'email': 'house@hospital.com',
            'phone': '1234567890'
        })
        
        dob_30_years_ago = date.today() - timedelta(days=30*365)
        self.patient = self.env['hr.hospital.patient'].create({
            'last_name': 'Doe',
            'first_name': 'John',
            'date_of_birth': dob_30_years_ago,
            'email': 'john.doe@test.com',
            'phone': '0987654321'
        })

    def test_compute_age(self):
        """1. Тестування методу _compute_age з hr.hospital.person"""
        
        self.patient._compute_age()
        self.assertTrue(self.patient.age >= 29 and self.patient.age <= 30, "Age computation failed.")
        
        self.patient.date_of_birth = False
        self.patient._compute_age()
        self.assertEqual(self.patient.age, 0, "Age should be 0 if no date of birth is set.")

    def test_check_email_validity(self):
        """2. Тестування методу _check_email_validity з hr.hospital.person"""

        self.patient.email = "valid.email@example.com"
        
        with self.assertRaises(ValidationError):
            self.patient.email = "invalid-email.com"
            self.patient._check_email_validity()

    def test_check_unique_visit_per_day(self):
        """3. Тестування методу _check_unique_visit_per_day з hr.hospital.visit"""
        visit_1 = self.env['hr.hospital.visit'].create({
            'doctor_id': self.doctor.id,
            'patient_id': self.patient.id,
            'visit_date_planned': date.today(),
            'state': 'planned'
        })
        self.assertTrue(visit_1.id, "First visit should be created successfully.")
        
        with self.assertRaises(ValidationError):
            self.env['hr.hospital.visit'].create({
                'doctor_id': self.doctor.id,
                'patient_id': self.patient.id,
                'visit_date_planned': date.today(),
                'state': 'planned'
            })