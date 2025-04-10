from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app import db
from models import Patient
from forms import PatientForm, PatientSearchForm

patients = Blueprint('patients', __name__, url_prefix='/patients')

@patients.route('/')
@login_required
def index():
    search_form = PatientSearchForm()
    patients_list = Patient.query.order_by(Patient.last_name).all()
    return render_template('patients/index.html', title='Patient List', patients=patients_list, search_form=search_form)

@patients.route('/new', methods=['GET', 'POST'])
@login_required
def new_patient():
    form = PatientForm()
    if form.validate_on_submit():
        patient = Patient(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            date_of_birth=form.date_of_birth.data,
            gender=form.gender.data,
            phone=form.phone.data,
            email=form.email.data,
            address=form.address.data,
            emergency_contact_name=form.emergency_contact_name.data,
            emergency_contact_phone=form.emergency_contact_phone.data,
            blood_type=form.blood_type.data,
            allergies=form.allergies.data,
            medical_conditions=form.medical_conditions.data
        )
        db.session.add(patient)
        db.session.commit()
        
        flash(f'Patient {patient.first_name} {patient.last_name} created successfully!', 'success')
        return redirect(url_for('patients.view', patient_id=patient.id))
        
    return render_template('patients/new.html', title='New Patient', form=form)

@patients.route('/<int:patient_id>')
@login_required
def view(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    return render_template('patients/view.html', title=f'Patient: {patient.get_full_name()}', patient=patient)

@patients.route('/<int:patient_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    form = PatientForm(obj=patient)
    
    if form.validate_on_submit():
        form.populate_obj(patient)
        db.session.commit()
        
        flash(f'Patient information updated successfully!', 'success')
        return redirect(url_for('patients.view', patient_id=patient.id))
        
    return render_template('patients/edit.html', title=f'Edit Patient: {patient.get_full_name()}', form=form, patient=patient)

@patients.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = PatientSearchForm()
    results = []
    
    if form.validate_on_submit() or request.args.get('search_term'):
        search_term = form.search_term.data or request.args.get('search_term')
        results = Patient.query.filter(
            (Patient.first_name.ilike(f'%{search_term}%')) |
            (Patient.last_name.ilike(f'%{search_term}%')) |
            (Patient.phone.ilike(f'%{search_term}%'))
        ).all()
        
    return render_template('patients/index.html', title='Patient Search', patients=results, search_form=form, search_term=form.search_term.data or request.args.get('search_term'))

@patients.route('/<int:patient_id>/delete', methods=['POST'])
@login_required
def delete(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    
    try:
        db.session.delete(patient)
        db.session.commit()
        flash(f'Patient {patient.get_full_name()} has been deleted.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Could not delete patient. The patient may have related records. Error: {str(e)}', 'danger')
    
    return redirect(url_for('patients.index'))