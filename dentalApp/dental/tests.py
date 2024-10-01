from django.test import TestCase
from django.urls import reverse
from .models import Clinic, Doctor, Patient

class ClinicTests(TestCase):
    def setUp(self):
        self.clinic = Clinic.objects.create(
            name="Test Clinic",
            phone_number="123-456-7890",
            city="Test City",
            state="Test State",
            address="123 Test St",
            email="test@clinic.com"
        )

        self.doctor = Doctor.objects.create(
            npi="1234567890",
            name="Dr. Smith",
            email="dr.smith@clinic.com",
            phone_number="098-765-4321",
            specialty="General",
        )
        self.doctor.clinic.add(self.clinic)  


        self.patient = Patient.objects.create(
            name="John Doe",
            date_of_birth="1990-01-01",
            phone_number="555-555-5555",
            address="456 Patient St",
            ssn_last_4="1234",
            gender="Male",
            doctor=self.doctor 
        )

    def test_add_clinic_view(self):
        response = self.client.post(reverse('add_clinic'), {
            'name': 'New Clinic',
            'phone_number': '987-654-3210',
            'city': 'New City',
            'state': 'New State',
            'address': '456 New St',
            'email': 'new@clinic.com',
        })

        self.assertRedirects(response, reverse('clinic_list'))
  
        self.assertTrue(Clinic.objects.filter(name='New Clinic').exists())

    def test_edit_clinic_view(self):
        response = self.client.post(reverse('clinic_detail', args=[self.clinic.id]), {
            'name': 'Updated Clinic',
            'phone_number': '111-222-3333',
            'city': 'Updated City',
            'state': 'Updated State',
            'address': '789 Updated St',
            'email': 'updated@clinic.com',
        })
       
        self.assertRedirects(response, reverse('clinic_detail', args=[self.clinic.id]))
        
        self.clinic.refresh_from_db()
        self.assertEqual(self.clinic.name, 'Updated Clinic')
        self.assertEqual(self.clinic.phone_number, '111-222-3333')
        self.assertEqual(self.clinic.city, 'Updated City')
        self.assertEqual(self.clinic.state, 'Updated State')
        self.assertEqual(self.clinic.address, '789 Updated St')
        self.assertEqual(self.clinic.email, 'updated@clinic.com')

class DoctorTests(TestCase):
    def setUp(self):
        
        self.clinic = Clinic.objects.create(
            name="Test Clinic",
            phone_number="123-456-7890",
            city="Test City",
            state="Test State",
            address="123 Test St",
            email="test@clinic.com"
        )

    def test_add_doctor_view(self):
        
        response = self.client.post(reverse('add_doctor'), {
            'npi': '1234567890',
            'name': 'Dr. Jones',
            'email': 'dr.jones@clinic.com',
            'phone_number': '123-456-7890',
            'office_address': 'Mountain view,CA', 
            'working_schedule': 'Mon-Fri 3 PM - 4 PM',
            'specialty': 'Cleaning'
        })
        
        self.assertRedirects(response, reverse('doctor_list'))
        
        self.assertTrue(Doctor.objects.filter(name='Dr. Jones').exists())

    def test_edit_doctor_view(self):
        
        doctor = Doctor.objects.create(
            npi="9876543210",
            name="Dr. Smith",
            email="dr.smith@clinic.com",
            phone_number="098-765-4321",
            office_address= "Mountain view,CA", 
            working_schedule= "Mon-Fri 1 PM - 4 PM",
            specialty="General"
        )
        doctor.clinic.add(self.clinic)

        response = self.client.post(reverse('doctor_detail', args=[doctor.id]), {
            'npi': '9876543210',
            'name': 'Dr. Smith Updated',
            'email': 'dr.smith.updated@clinic.com',
            'phone_number': '111-222-3333',
            'office_address': 'Mountain view,CA', 
            'working_schedule': 'Mon-Fri 3 PM - 4 PM',
            'clinic': [self.clinic.id],
        })
        
        self.assertRedirects(response, reverse('doctor_detail', args=[doctor.id]))
       
        doctor.refresh_from_db()
        self.assertEqual(doctor.name, 'Dr. Smith Updated')
        self.assertEqual(doctor.email, 'dr.smith.updated@clinic.com')
        self.assertEqual(doctor.phone_number, '111-222-3333')
        self.assertEqual(doctor.specialty, 'General')

class PatientTests(TestCase):
    def setUp(self):
        
        self.clinic = Clinic.objects.create(
            name="Test Clinic",
            phone_number="123-456-7890",
            city="Test City",
            state="Test State",
            address="123 Test St",
            email="test@clinic.com"
        )

        
        self.doctor = Doctor.objects.create(
            npi="1234567890",
            name="Dr. Smith",
            email="dr.smith@clinic.com",
            phone_number="098-765-4321",
            specialty="General",
        )
        self.doctor.clinic.add(self.clinic)

    def test_add_patient_view(self):
        
        response = self.client.post(reverse('add_patient'), {
            'name': 'Jane Doe',
            'date_of_birth': '1995-05-05',
            'phone_number': '555-555-5555',
            'address': '789 Patient Ave',
            'ssn_last_4': '5678',
            'gender': 'Female',
            'doctor': self.doctor.id,  
        })
    
        self.assertRedirects(response, reverse('patient_list'))

        self.assertTrue(Patient.objects.filter(name='Jane Doe').exists())

    def test_edit_patient_view(self):
        patient = Patient.objects.create(
            name="John Doe",
            date_of_birth="1990-01-01",
            phone_number="555-555-5555",
            address="456 Patient St",
            ssn_last_4="1234",
            gender="Male",
            doctor=self.doctor
        )

        response = self.client.post(reverse('patient_detail', args=[patient.id]), {
            'name': 'John Doe Updated',
            'date_of_birth': '1990-01-01',
            'phone_number': '111-222-3333',
            'address': '789 Updated Patient St',
            'ssn_last_4': '4321',
            'gender': 'Male',
            'doctor': self.doctor.id,
        })

        self.assertRedirects(response, reverse('patient_detail', args=[patient.id]))

        patient.refresh_from_db()
        self.assertEqual(patient.name, 'John Doe Updated')
        self.assertEqual(patient.phone_number, '111-222-3333')
        self.assertEqual(patient.address, '789 Updated Patient St')
        self.assertEqual(patient.ssn_last_4, '4321')
