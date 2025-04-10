from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from app import db
from models import ClinicalNote, Patient
from forms import ClinicalNoteForm

clinical = Blueprint('clinical', __name__, url_prefix='/clinical')

@clinical.route('/notes')
@login_required
def notes():
    notes_list = ClinicalNote.query.order_by(ClinicalNote.created_at.desc()).all()
    return render_template('clinical/notes.html', title='Clinical Notes', notes=notes_list)

@clinical.route('/notes/new', methods=['GET', 'POST'])
@login_required
def new_note():
    form = ClinicalNoteForm()
    
    # Populate patient dropdown
    form.patient_id.choices = [(p.id, p.get_full_name()) for p in Patient.query.order_by(Patient.last_name).all()]
    
    # Pre-fill patient if provided in query string
    if request.args.get('patient_id'):
        try:
            form.patient_id.data = int(request.args.get('patient_id'))
        except:
            pass
    
    if form.validate_on_submit():
        note = ClinicalNote(
            patient_id=form.patient_id.data,
            author_id=current_user.id,
            note_type=form.note_type.data,
            content=form.content.data,
            diagnosis=form.diagnosis.data,
            treatment_plan=form.treatment_plan.data
        )
        
        db.session.add(note)
        db.session.commit()
        
        flash('Clinical note created successfully!', 'success')
        return redirect(url_for('clinical.view_note', note_id=note.id))
        
    return render_template('clinical/new_note.html', title='New Clinical Note', form=form)

@clinical.route('/notes/<int:note_id>')
@login_required
def view_note(note_id):
    note = ClinicalNote.query.get_or_404(note_id)
    return render_template('clinical/view_note.html', title='Clinical Note', note=note)

@clinical.route('/notes/<int:note_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_note(note_id):
    note = ClinicalNote.query.get_or_404(note_id)
    
    # Only the author can edit the note
    if note.author_id != current_user.id:
        flash('You can only edit notes that you created.', 'warning')
        return redirect(url_for('clinical.view_note', note_id=note.id))
    
    form = ClinicalNoteForm(obj=note)
    
    # Populate patient dropdown
    form.patient_id.choices = [(p.id, p.get_full_name()) for p in Patient.query.order_by(Patient.last_name).all()]
    
    if form.validate_on_submit():
        form.populate_obj(note)
        db.session.commit()
        
        flash('Clinical note updated successfully!', 'success')
        return redirect(url_for('clinical.view_note', note_id=note.id))
        
    return render_template('clinical/edit_note.html', title='Edit Clinical Note', form=form, note=note)

@clinical.route('/diagnosis')
@login_required
def diagnosis():
    patient_id = request.args.get('patient_id', None)
    if patient_id:
        patient = Patient.query.get_or_404(patient_id)
        notes = ClinicalNote.query.filter_by(patient_id=patient_id).order_by(ClinicalNote.created_at.desc()).all()
        return render_template('clinical/diagnosis.html', title=f'Diagnosis History: {patient.get_full_name()}', patient=patient, notes=notes)
    
    return redirect(url_for('patients.index'))