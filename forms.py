from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms import DateField, DateTimeField, TimeField, IntegerField, DecimalField, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from datetime import date
from models import User, Patient

# Authentication Forms
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists. Please choose a different one.')

# Patient Forms
class PatientForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    date_of_birth = DateField('Date of Birth', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    phone = StringField('Phone Number')
    email = StringField('Email', validators=[Optional(), Email()])
    address = TextAreaField('Address')
    emergency_contact_name = StringField('Emergency Contact Name')
    emergency_contact_phone = StringField('Emergency Contact Phone')
    blood_type = SelectField('Blood Type', choices=[
        ('', 'Select Blood Type'), 
        ('A+', 'A+'), ('A-', 'A-'), 
        ('B+', 'B+'), ('B-', 'B-'), 
        ('AB+', 'AB+'), ('AB-', 'AB-'), 
        ('O+', 'O+'), ('O-', 'O-')
    ])
    allergies = TextAreaField('Allergies')
    medical_conditions = TextAreaField('Medical Conditions')
    submit = SubmitField('Save Patient')

    def validate_date_of_birth(self, date_of_birth):
        if date_of_birth.data > date.today():
            raise ValidationError('Date of birth cannot be in the future.')

class PatientSearchForm(FlaskForm):
    search_term = StringField('Search by Name, ID, or Phone', validators=[DataRequired()])
    submit = SubmitField('Search')

# Appointment Forms
class AppointmentForm(FlaskForm):
    patient_id = SelectField('Patient', coerce=int, validators=[DataRequired()])
    staff_id = SelectField('Doctor/Staff', coerce=int, validators=[DataRequired()])
    title = StringField('Appointment Title', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    start_time = TimeField('Start Time', validators=[DataRequired()])
    end_time = TimeField('End Time', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('scheduled', 'Scheduled'), 
        ('completed', 'Completed'), 
        ('cancelled', 'Cancelled'), 
        ('no-show', 'No Show')
    ])
    notes = TextAreaField('Notes')
    submit = SubmitField('Save Appointment')

    def validate_date(self, date):
        if date.data < date.today():
            raise ValidationError('Appointment date cannot be in the past.')

# Clinical Notes Forms
class ClinicalNoteForm(FlaskForm):
    patient_id = SelectField('Patient', coerce=int, validators=[DataRequired()])
    note_type = SelectField('Note Type', choices=[
        ('progress', 'Progress Note'), 
        ('admission', 'Admission Note'),
        ('discharge', 'Discharge Summary'),
        ('consultation', 'Consultation'),
        ('procedure', 'Procedure Note'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    content = TextAreaField('Clinical Notes', validators=[DataRequired()])
    diagnosis = TextAreaField('Diagnosis')
    treatment_plan = TextAreaField('Treatment Plan')
    submit = SubmitField('Save Note')

# Prescription Forms
class PrescriptionForm(FlaskForm):
    patient_id = SelectField('Patient', coerce=int, validators=[DataRequired()])
    prescription_date = DateField('Prescription Date', validators=[DataRequired()])
    notes = TextAreaField('Notes')
    status = SelectField('Status', choices=[
        ('active', 'Active'), 
        ('completed', 'Completed'), 
        ('cancelled', 'Cancelled')
    ])
    submit = SubmitField('Save Prescription')

class PrescriptionItemForm(FlaskForm):
    medication_id = SelectField('Medication', coerce=int, validators=[DataRequired()])
    dosage = StringField('Dosage', validators=[DataRequired()])
    frequency = StringField('Frequency', validators=[DataRequired()])
    duration = StringField('Duration', validators=[DataRequired()])
    instructions = TextAreaField('Instructions')
    submit = SubmitField('Add Medication')

# Laboratory Forms
class LabResultForm(FlaskForm):
    patient_id = SelectField('Patient', coerce=int, validators=[DataRequired()])
    test_id = SelectField('Test', coerce=int, validators=[DataRequired()])
    result_value = StringField('Result', validators=[DataRequired()])
    test_date = DateField('Test Date', validators=[DataRequired()])
    is_abnormal = BooleanField('Abnormal Result')
    notes = TextAreaField('Notes')
    submit = SubmitField('Save Result')

# Document Forms
class DocumentForm(FlaskForm):
    patient_id = SelectField('Patient', coerce=int, validators=[DataRequired()])
    title = StringField('Document Title', validators=[DataRequired()])
    document_type = SelectField('Document Type', choices=[
        ('lab_report', 'Lab Report'),
        ('consent_form', 'Consent Form'),
        ('discharge_summary', 'Discharge Summary'),
        ('referral', 'Referral Letter'),
        ('imaging', 'Imaging'),
        ('other', 'Other')
    ])
    file = FileField('Document File', validators=[DataRequired()])
    notes = TextAreaField('Notes')
    submit = SubmitField('Upload Document')

# Billing Forms
class InvoiceForm(FlaskForm):
    patient_id = SelectField('Patient', coerce=int, validators=[DataRequired()])
    invoice_date = DateField('Invoice Date', validators=[DataRequired()])
    due_date = DateField('Due Date', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled')
    ])
    payment_method = SelectField('Payment Method', choices=[
        ('', 'Select Payment Method'),
        ('cash', 'Cash'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('insurance', 'Insurance'),
        ('bank_transfer', 'Bank Transfer'),
        ('other', 'Other')
    ])
    notes = TextAreaField('Notes')
    submit = SubmitField('Save Invoice')

class InvoiceItemForm(FlaskForm):
    description = StringField('Description', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    unit_price = DecimalField('Unit Price', validators=[DataRequired()])
    submit = SubmitField('Add Item')
