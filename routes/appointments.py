from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime, date

from app import db
from models import Appointment, Patient, User
from forms import AppointmentForm

appointments = Blueprint('appointments', __name__, url_prefix='/appointments')

@appointments.route('/')
@login_required
def index():
    today = date.today()
    appointments_list = Appointment.query.filter_by(date=today).order_by(Appointment.start_time).all()
    return render_template('appointments/index.html', title='Today\'s Appointments', appointments=appointments_list)

@appointments.route('/calendar')
@login_required
def calendar():
    return render_template('appointments/calendar.html', title='Appointment Calendar')

@appointments.route('/json')
@login_required
def get_appointments_json():
    appointments_list = Appointment.query.all()
    events = []
    
    for appointment in appointments_list:
        events.append({
            'id': appointment.id,
            'title': appointment.title,
            'start': f"{appointment.date.isoformat()}T{appointment.start_time.isoformat()}",
            'end': f"{appointment.date.isoformat()}T{appointment.end_time.isoformat()}",
            'extendedProps': {
                'status': appointment.status,
                'patient': appointment.patient.get_full_name(),
                'doctor': appointment.staff.get_full_name()
            },
            'classNames': f"status-{appointment.status}"
        })
    
    return jsonify(events)

@appointments.route('/new', methods=['GET', 'POST'])
@login_required
def new_appointment():
    form = AppointmentForm()
    
    # Populate select fields
    form.patient_id.choices = [(p.id, p.get_full_name()) for p in Patient.query.order_by(Patient.last_name).all()]
    form.staff_id.choices = [(s.id, s.get_full_name()) for s in User.query.order_by(User.last_name).all()]
    
    # Pre-fill date if provided in query string
    if request.args.get('date'):
        try:
            form.date.data = datetime.strptime(request.args.get('date'), '%Y-%m-%d').date()
        except:
            pass
    
    if form.validate_on_submit():
        appointment = Appointment(
            patient_id=form.patient_id.data,
            staff_id=form.staff_id.data,
            title=form.title.data,
            date=form.date.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            status=form.status.data,
            notes=form.notes.data
        )
        
        db.session.add(appointment)
        db.session.commit()
        
        flash('Appointment created successfully!', 'success')
        return redirect(url_for('appointments.index'))
        
    return render_template('appointments/new.html', title='New Appointment', form=form)

@appointments.route('/<int:appointment_id>')
@login_required
def view(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    return render_template('appointments/view.html', title=f'Appointment Details', appointment=appointment)

@appointments.route('/<int:appointment_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    form = AppointmentForm(obj=appointment)
    
    # Populate select fields
    form.patient_id.choices = [(p.id, p.get_full_name()) for p in Patient.query.order_by(Patient.last_name).all()]
    form.staff_id.choices = [(s.id, s.get_full_name()) for s in User.query.order_by(User.last_name).all()]
    
    if form.validate_on_submit():
        form.populate_obj(appointment)
        db.session.commit()
        
        flash('Appointment updated successfully!', 'success')
        return redirect(url_for('appointments.view', appointment_id=appointment.id))
        
    return render_template('appointments/edit.html', title='Edit Appointment', form=form, appointment=appointment)

@appointments.route('/<int:appointment_id>/cancel', methods=['POST'])
@login_required
def cancel(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    appointment.status = 'cancelled'
    db.session.commit()
    
    flash('Appointment has been cancelled.', 'success')
    return redirect(url_for('appointments.calendar'))