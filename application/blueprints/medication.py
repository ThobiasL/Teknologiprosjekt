from flask import Blueprint, flash, request, redirect, url_for, render_template # Importerer nødvendige funksjoner fra Flask
from core.models.medication import Medication
from core.utils import is_valid_time

# Lager blueprint for 'medication'
medication = Blueprint('medication', __name__)

# Funksjon for å vise medisinsiden
@medication.route('/medication')
def show_page():
    medication = Medication.get_by_id(Medication, 1)

    if not medication:
        return redirect(url_for('main.home'))

    time = medication.get('time')
    return render_template('medication.html', time=time)

# Funksjon for å oppdatere medisintid
@medication.route('/update_medication_time', methods=['POST'])
def update_medication_time():
    medication = Medication.get_by_id(Medication, 1)
    time = request.form.get('time')

    if not is_valid_time(time):
        flash('Ugyldig tid', 'error')
        return redirect(url_for('medication.show_page'))
    
    medication.set('time', time)
    flash('Medisintid endret', 'message')
    return redirect(url_for('medication.show_page'))