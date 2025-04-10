from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app import db
from models import Prescription, PrescriptionItem, Patient, Medication
from forms import PrescriptionForm, PrescriptionItemForm

prescriptions = Blueprint('prescriptions', __name__, url_prefix='/prescriptions')

@prescriptions.route('/')
@login_required
def index():
    prescriptions_list = Prescription.query.order_by(Prescription.prescription_date.desc()).all()
    return render_template('prescriptions/index.html', title='Prescriptions', prescriptions=prescriptions_list)

@prescriptions.route('/new', methods=['GET', 'POST'])
@login_required
def new_prescription():
    form = PrescriptionForm()
    
    # Populate patient dropdown
    form.patient_id.choices = [(p.id, p.get_full_name()) for p in Patient.query.order_by(Patient.last_name).all()]
    
    # Pre-fill patient if provided in query string
    if request.args.get('patient_id'):
        try:
            form.patient_id.data = int(request.args.get('patient_id'))
        except:
            pass
    
    if form.validate_on_submit():
        prescription = Prescription(
            patient_id=form.patient_id.data,
            prescribed_by_id=current_user.id,
            prescription_date=form.prescription_date.data,
            notes=form.notes.data,
            status=form.status.data
        )
        
        db.session.add(prescription)
        db.session.commit()
        
        flash('Prescription created successfully! Now add medications to the prescription.', 'success')
        return redirect(url_for('prescriptions.view', prescription_id=prescription.id))
        
    return render_template('prescriptions/new.html', title='New Prescription', form=form)

@prescriptions.route('/<int:prescription_id>')
@login_required
def view(prescription_id):
    prescription = Prescription.query.get_or_404(prescription_id)
    medication_form = PrescriptionItemForm()
    medication_form.medication_id.choices = [(m.id, m.name) for m in Medication.query.order_by(Medication.name).all()]
    
    return render_template('prescriptions/view.html', title='Prescription Details', 
                           prescription=prescription, medication_form=medication_form)

@prescriptions.route('/<int:prescription_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(prescription_id):
    prescription = Prescription.query.get_or_404(prescription_id)
    
    # Cannot edit completed or cancelled prescriptions
    if prescription.status != 'active':
        flash('Cannot edit a completed or cancelled prescription.', 'warning')
        return redirect(url_for('prescriptions.view', prescription_id=prescription.id))
    
    form = PrescriptionForm(obj=prescription)
    
    # Populate patient dropdown
    form.patient_id.choices = [(p.id, p.get_full_name()) for p in Patient.query.order_by(Patient.last_name).all()]
    
    if form.validate_on_submit():
        form.populate_obj(prescription)
        db.session.commit()
        
        flash('Prescription updated successfully!', 'success')
        return redirect(url_for('prescriptions.view', prescription_id=prescription.id))
        
    return render_template('prescriptions/edit.html', title='Edit Prescription', form=form, prescription=prescription)

@prescriptions.route('/<int:prescription_id>/add_medication', methods=['POST'])
@login_required
def add_medication(prescription_id):
    prescription = Prescription.query.get_or_404(prescription_id)
    
    # Cannot edit completed or cancelled prescriptions
    if prescription.status != 'active':
        flash('Cannot add medications to a completed or cancelled prescription.', 'warning')
        return redirect(url_for('prescriptions.view', prescription_id=prescription.id))
    
    form = PrescriptionItemForm()
    form.medication_id.choices = [(m.id, m.name) for m in Medication.query.order_by(Medication.name).all()]
    
    if form.validate_on_submit():
        # Calculate item total
        medication_item = PrescriptionItem(
            prescription_id=prescription.id,
            medication_id=form.medication_id.data,
            dosage=form.dosage.data,
            frequency=form.frequency.data,
            duration=form.duration.data,
            instructions=form.instructions.data
        )
        
        db.session.add(medication_item)
        db.session.commit()
        
        flash('Medication added to prescription.', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {getattr(form, field).label.text}: {error}', 'danger')
    
    return redirect(url_for('prescriptions.view', prescription_id=prescription.id))

@prescriptions.route('/<int:prescription_id>/remove_medication/<int:item_id>', methods=['POST'])
@login_required
def remove_medication(prescription_id, item_id):
    prescription = Prescription.query.get_or_404(prescription_id)
    
    # Cannot edit completed or cancelled prescriptions
    if prescription.status != 'active':
        flash('Cannot remove medications from a completed or cancelled prescription.', 'warning')
        return redirect(url_for('prescriptions.view', prescription_id=prescription.id))
    
    medication_item = PrescriptionItem.query.get_or_404(item_id)
    
    # Verify the item belongs to this prescription
    if medication_item.prescription_id != prescription.id:
        flash('Invalid medication item.', 'danger')
        return redirect(url_for('prescriptions.view', prescription_id=prescription.id))
    
    db.session.delete(medication_item)
    db.session.commit()
    
    flash('Medication removed from prescription.', 'success')
    return redirect(url_for('prescriptions.view', prescription_id=prescription.id))

@prescriptions.route('/<int:prescription_id>/change_status/<status>', methods=['POST'])
@login_required
def change_status(prescription_id, status):
    prescription = Prescription.query.get_or_404(prescription_id)
    
    if status not in ['active', 'completed', 'cancelled']:
        flash('Invalid status.', 'danger')
        return redirect(url_for('prescriptions.view', prescription_id=prescription.id))
    
    prescription.status = status
    db.session.commit()
    
    flash(f'Prescription status changed to {status}.', 'success')
    return redirect(url_for('prescriptions.view', prescription_id=prescription.id))