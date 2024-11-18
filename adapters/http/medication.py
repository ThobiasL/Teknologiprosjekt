from flask import Blueprint, flash, request, redirect, url_for, render_template # Importerer nødvendige funksjoner fra Flask
from adapters.database.medication_flask import Medication
from core.utils import is_valid_time

# Lager blueprint for 'medication'
medication = Blueprint('medication', __name__)

# Viser dagene
@medication.route('/medication')
def show_page():
    days = Medication.query.all()
    return render_template('medication.html', days=days)

@medication.route('/medication/<int:medication_id>')
def medication_day(medication_id):
    medication = Medication.get_by_id(Medication, medication_id)
    if not medication:
        return redirect(url_for('medication.show_page'))

    # For hver dose på en gitt dag, hent tid og status
    doses = [
        {
            'dose_id': i,
            'time': medication.get(f'dose_{i}'),
            'scheduled': medication.get(f'scheduled_{i}')
        } for i in range(1, 5)
    ]

    # Vis oversikt over dosene for den valgte dagen
    return render_template('medication_day.html', medication=medication, doses=doses)


@medication.route('/medication/<int:medication_id>/<int:dose_id>', methods=['GET', 'POST'])
def medication_dose(medication_id, dose_id):
    medication = Medication.get_by_id(Medication, medication_id)
    if not medication or dose_id not in range(1, 5):
        return redirect(url_for('medication.show_page'))

    # Håndter POST-forespørsel
    if request.method == 'POST':
        # Hvis brukeren vil sette tid for dosen
        if 'set_time' in request.form:
            time = request.form.get('time')
            if is_valid_time(time):
                medication.set(f'dose_{dose_id}', time)
                medication.set(f'scheduled_{dose_id}', True)
                flash(f'Doseringstid endret', 'success')
            else:
                flash('Ugyldig tid', 'error')

        # Hvis brukeren vil aktivere/deaktivere dosen
        elif 'toggle_schedule' in request.form:
            current_status = medication.get(f'scheduled_{dose_id}')
            medication.set(f'scheduled_{dose_id}', not current_status)  # Veksler status
            flash(f"Dose {'aktivert' if not current_status else 'deaktivert'}", 'success')

        # Lagre alle endringer
        medication.save()
        return redirect(url_for('medication.medication_dose', medication_id=medication_id, dose_id=dose_id))

    # Hent oppdatert informasjon for visning
    time = medication.get(f'dose_{dose_id}')
    scheduled = medication.get(f'scheduled_{dose_id}')
    return render_template('medication_dose.html', medication=medication, dose_id=dose_id, time=time, scheduled=scheduled)
