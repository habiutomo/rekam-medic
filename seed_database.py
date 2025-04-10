"""
Seed database script.

This script populates the database with initial data for testing and development.
It creates roles, users, patients, medications, and lab tests.
"""

import os
import sys
from datetime import datetime, date, timedelta
from werkzeug.security import generate_password_hash

from app import db, app
from models import Role, User, Patient, Medication, LabTest

def create_roles():
    """Create default roles."""
    roles = [
        {'name': 'admin', 'description': 'Administrator with full access'},
        {'name': 'doctor', 'description': 'Physician with clinical access'},
        {'name': 'nurse', 'description': 'Nurse with patient care access'},
        {'name': 'receptionist', 'description': 'Front desk staff for appointments and registration'},
        {'name': 'lab_tech', 'description': 'Laboratory technician for test results'},
        {'name': 'billing', 'description': 'Billing and finance staff'}
    ]
    
    for role_data in roles:
        role = Role.query.filter_by(name=role_data['name']).first()
        if not role:
            role = Role(**role_data)
            db.session.add(role)
    
    db.session.commit()
    print("Roles created successfully.")
    
def create_users():
    """Create default users with different roles."""
    # Get role IDs
    admin_role = Role.query.filter_by(name='admin').first()
    doctor_role = Role.query.filter_by(name='doctor').first()
    nurse_role = Role.query.filter_by(name='nurse').first()
    receptionist_role = Role.query.filter_by(name='receptionist').first()
    lab_tech_role = Role.query.filter_by(name='lab_tech').first()
    billing_role = Role.query.filter_by(name='billing').first()
    
    users = [
        {
            'username': 'admin',
            'email': 'admin@example.com',
            'password': 'admin1234',
            'first_name': 'System',
            'last_name': 'Administrator',
            'role_id': admin_role.id
        },
        {
            'username': 'doctor',
            'email': 'doctor@example.com',
            'password': 'doctor1234',
            'first_name': 'John',
            'last_name': 'Smith',
            'role_id': doctor_role.id
        },
        {
            'username': 'nurse',
            'email': 'nurse@example.com',
            'password': 'nurse1234',
            'first_name': 'Sarah',
            'last_name': 'Johnson',
            'role_id': nurse_role.id
        },
        {
            'username': 'receptionist',
            'email': 'receptionist@example.com',
            'password': 'reception1234',
            'first_name': 'Emma',
            'last_name': 'Davis',
            'role_id': receptionist_role.id
        },
        {
            'username': 'labtech',
            'email': 'labtech@example.com',
            'password': 'labtech1234',
            'first_name': 'Michael',
            'last_name': 'Lee',
            'role_id': lab_tech_role.id
        },
        {
            'username': 'billing',
            'email': 'billing@example.com',
            'password': 'billing1234',
            'first_name': 'Robert',
            'last_name': 'Wilson',
            'role_id': billing_role.id
        }
    ]
    
    for user_data in users:
        user = User.query.filter_by(username=user_data['username']).first()
        if not user:
            # Store original password
            password = user_data.pop('password')
            # Create user
            user = User(**user_data)
            user.password_hash = generate_password_hash(password)
            db.session.add(user)
    
    db.session.commit()
    print("Users created successfully.")

def create_sample_patients():
    """Create sample patients for testing."""
    patients = [
        {
            'first_name': 'John',
            'last_name': 'Doe',
            'date_of_birth': date(1980, 5, 15),
            'gender': 'Male',
            'phone': '555-123-4567',
            'email': 'john.doe@example.com',
            'address': '123 Main St, Anytown, CA 12345',
            'emergency_contact_name': 'Jane Doe',
            'emergency_contact_phone': '555-987-6543',
            'blood_type': 'A+',
            'allergies': 'Penicillin',
            'medical_conditions': 'Hypertension, Diabetes Type 2'
        },
        {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'date_of_birth': date(1992, 8, 22),
            'gender': 'Female',
            'phone': '555-222-3333',
            'email': 'jane.smith@example.com',
            'address': '456 Oak Ave, Somewhere, NY 54321',
            'emergency_contact_name': 'John Smith',
            'emergency_contact_phone': '555-444-5555',
            'blood_type': 'O-',
            'allergies': 'Sulfa drugs, Peanuts',
            'medical_conditions': 'Asthma'
        },
        {
            'first_name': 'Robert',
            'last_name': 'Johnson',
            'date_of_birth': date(1975, 3, 10),
            'gender': 'Male',
            'phone': '555-666-7777',
            'email': 'robert.j@example.com',
            'address': '789 Pine St, Elsewhere, TX 67890',
            'emergency_contact_name': 'Mary Johnson',
            'emergency_contact_phone': '555-888-9999',
            'blood_type': 'B+',
            'allergies': 'None',
            'medical_conditions': 'Arthritis, High Cholesterol'
        },
        {
            'first_name': 'Maria',
            'last_name': 'Garcia',
            'date_of_birth': date(1988, 11, 3),
            'gender': 'Female',
            'phone': '555-111-2222',
            'email': 'maria.g@example.com',
            'address': '321 Elm St, Nowhere, FL 13579',
            'emergency_contact_name': 'Carlos Garcia',
            'emergency_contact_phone': '555-333-4444',
            'blood_type': 'AB+',
            'allergies': 'Latex, Shellfish',
            'medical_conditions': 'Migraine'
        },
        {
            'first_name': 'David',
            'last_name': 'Wilson',
            'date_of_birth': date(1965, 7, 28),
            'gender': 'Male',
            'phone': '555-555-6666',
            'email': 'david.w@example.com',
            'address': '654 Maple Ave, Anyplace, WA 97531',
            'emergency_contact_name': 'Susan Wilson',
            'emergency_contact_phone': '555-777-8888',
            'blood_type': 'A-',
            'allergies': 'Ibuprofen',
            'medical_conditions': 'COPD, Hypertension'
        }
    ]
    
    for patient_data in patients:
        patient = Patient.query.filter_by(email=patient_data['email']).first()
        if not patient:
            patient = Patient(**patient_data)
            db.session.add(patient)
    
    db.session.commit()
    print("Sample patients created successfully.")

def create_medications():
    """Create common medications."""
    medications = [
        {
            'name': 'Amoxicillin',
            'description': 'Antibiotic used to treat bacterial infections',
            'dosage_form': 'tablet',
            'manufacturer': 'Generic'
        },
        {
            'name': 'Lisinopril',
            'description': 'ACE inhibitor used to treat high blood pressure',
            'dosage_form': 'tablet',
            'manufacturer': 'Generic'
        },
        {
            'name': 'Metformin',
            'description': 'Oral diabetes medicine that helps control blood sugar levels',
            'dosage_form': 'tablet',
            'manufacturer': 'Generic'
        },
        {
            'name': 'Atorvastatin',
            'description': 'Statin medication used to lower blood cholesterol',
            'dosage_form': 'tablet',
            'manufacturer': 'Generic'
        },
        {
            'name': 'Albuterol',
            'description': 'Bronchodilator that relaxes muscles in the airways',
            'dosage_form': 'inhaler',
            'manufacturer': 'Generic'
        },
        {
            'name': 'Omeprazole',
            'description': 'Proton pump inhibitor used to treat acid reflux and ulcers',
            'dosage_form': 'capsule',
            'manufacturer': 'Generic'
        },
        {
            'name': 'Ibuprofen',
            'description': 'Nonsteroidal anti-inflammatory drug used for pain relief',
            'dosage_form': 'tablet',
            'manufacturer': 'Generic'
        },
        {
            'name': 'Acetaminophen',
            'description': 'Pain reliever and fever reducer',
            'dosage_form': 'tablet',
            'manufacturer': 'Generic'
        },
        {
            'name': 'Fluoxetine',
            'description': 'Selective serotonin reuptake inhibitor used to treat depression',
            'dosage_form': 'capsule',
            'manufacturer': 'Generic'
        },
        {
            'name': 'Levothyroxine',
            'description': 'Synthetic thyroid hormone used to treat hypothyroidism',
            'dosage_form': 'tablet',
            'manufacturer': 'Generic'
        }
    ]
    
    for med_data in medications:
        medication = Medication.query.filter_by(name=med_data['name']).first()
        if not medication:
            medication = Medication(**med_data)
            db.session.add(medication)
    
    db.session.commit()
    print("Medications created successfully.")

def create_lab_tests():
    """Create common laboratory tests."""
    lab_tests = [
        {
            'name': 'Complete Blood Count (CBC)',
            'description': 'Measures the levels of red blood cells, white blood cells, and platelets',
            'normal_range': 'Varies by component',
            'unit': 'Various'
        },
        {
            'name': 'Basic Metabolic Panel (BMP)',
            'description': 'Measures glucose, calcium, and electrolyte levels',
            'normal_range': 'Varies by component',
            'unit': 'Various'
        },
        {
            'name': 'Lipid Panel',
            'description': 'Measures cholesterol and triglyceride levels',
            'normal_range': 'Total Cholesterol: <200 mg/dL',
            'unit': 'mg/dL'
        },
        {
            'name': 'Liver Function Tests',
            'description': 'Measures enzymes and proteins that reflect liver function',
            'normal_range': 'ALT: 7-55 U/L, AST: 8-48 U/L',
            'unit': 'U/L'
        },
        {
            'name': 'Hemoglobin A1C',
            'description': 'Measures average blood glucose over the past 2-3 months',
            'normal_range': '4.0-5.6%',
            'unit': '%'
        },
        {
            'name': 'Thyroid Stimulating Hormone (TSH)',
            'description': 'Measures thyroid function',
            'normal_range': '0.4-4.0 mIU/L',
            'unit': 'mIU/L'
        },
        {
            'name': 'Urinalysis',
            'description': 'Analyzes the physical, chemical, and microscopic properties of urine',
            'normal_range': 'Varies by component',
            'unit': 'Various'
        },
        {
            'name': 'Vitamin D',
            'description': 'Measures vitamin D levels',
            'normal_range': '20-50 ng/mL',
            'unit': 'ng/mL'
        },
        {
            'name': 'C-Reactive Protein (CRP)',
            'description': 'Measures inflammation in the body',
            'normal_range': '<10 mg/L',
            'unit': 'mg/L'
        },
        {
            'name': 'COVID-19 PCR Test',
            'description': 'Detects genetic material of the SARS-CoV-2 virus',
            'normal_range': 'Negative',
            'unit': 'N/A'
        }
    ]
    
    for test_data in lab_tests:
        lab_test = LabTest.query.filter_by(name=test_data['name']).first()
        if not lab_test:
            lab_test = LabTest(**test_data)
            db.session.add(lab_test)
    
    db.session.commit()
    print("Lab tests created successfully.")

def main():
    """Execute seed functions."""
    with app.app_context():
        print("Starting database seeding...")
        create_roles()
        create_users()
        create_sample_patients()
        create_medications()
        create_lab_tests()
        print("Database seeding completed successfully!")

if __name__ == "__main__":
    main()