from flask import Blueprint, flash, request, redirect, url_for, render_template # Importerer nødvendige funksjoner fra Flask
from adapters.database.medication import Medication
from core.utils import is_valid_time

# Lager blueprint for 'medication'
medication = Blueprint('medication', __name__)

# Funksjon for å vise medisinsiden
@medication.route('/medication')
def show_page():
    days = Medication.query.all()
    return render_template('medication.html', days=days)

@medication.route('/medication/<int:medication_id>', methods=['GET', 'POST'])
def medication_detail(medication_id):
    medication = Medication.get_by_id(Medication, medication_id)
    if not medication:
        return redirect(url_for('medication.show_page'))
    
    return render_template('medication_detail.html', medication=medication)

# Funksjon for å oppdatere medisintid
@medication.route('/medication/<int:medication_id>/set_time/', methods=['POST'])
def set_time(medication_id):
    medication = Medication.get_by_id(Medication, medication_id)
    time = request.form.get('time')

    if not is_valid_time(time):
        flash('Ugyldig tid', 'error')
        return redirect(url_for('medication.medication_detail', medication_id=medication_id))
    
    medication.set('time', time)
    flash('Medisintid endret', 'message')
    return redirect(url_for('medication.medication_detail', medication_id=medication_id))

@medication.route('/medication/<int:medication_id>/toggle_schedule', methods=['POST'])
def toggle_schedule(medication_id):
     
    medication = Medication.get_by_id(Medication, medication_id)

    if not medication:
        return redirect(url_for('medication.show_page'))
    
    medication.set('scheduled', not medication.get('scheduled'))
    return redirect(url_for('medication.medication_detail', medication_id=medication_id))
